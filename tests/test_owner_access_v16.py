"""V16 owner/auth/content regression tests using a real local HTTP server."""
import copy
import hashlib
import http.client
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from portable import server as APP
from portable.owner_admin import provision, verifier, validate_verifier, write_bootstrap


class OwnerAccessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.public = self.root / "public"
        self.public.mkdir()
        (self.public / "index.html").write_text("<!doctype html><title>Fixture</title>")
        self.course = {"id": "test-rail", "title": "Rail", "titleEn": "Rail", "category": "rail",
                       "stages": [{"id": "trial", "steps": [{"id": "s1", "instruction": "FREE_FIRST_STAGE", "quiz": {"answer": 0}}]},
                                  {"id": "member", "steps": [{"id": "s2", "instruction": "MEMBER_BODY_SENTINEL", "quiz": {"answer": 1}}]}]}
        preview = copy.deepcopy(self.course)
        preview["publicStub"] = True
        preview["previewOnly"] = True
        preview["freeStagesPerCourse"] = 1
        preview["stages"][1]["steps"] = [{"id": "s2", "locked": True}]
        index_course = {**{k: v for k, v in self.course.items() if k != "stages"}, "_lazy": True,
                        "stages": [{"id": t["id"], "steps": [{"id": s["id"]} for s in t["steps"]]} for t in self.course["stages"]]}
        full_resources = {"sources": [], "media": {"courses": [{"courseId":"test-rail","videos": [], "guides": [{"text": "MEMBER_GUIDE_SENTINEL"}]}]}}
        resources = {"sources": [], "media": {"courses": [{"courseId":"test-rail","videos": [], "guides": []}]}}
        self.full_descriptor = self.chunk("owner-courses", self.course)
        self.private_resources = self.chunk("owner-resources", full_resources)
        public_descriptor = self.public_descriptor = self.chunk("courses", preview)
        public_resources = self.public_resources = self.chunk("resources", resources)
        lazy = self.public / "data/lazy"
        (lazy / "index.json").write_text(json.dumps({"catalog": [index_course], "courses": {"test-rail": public_descriptor}, "resources": {"test-rail": public_resources}}))
        (lazy / "index.compact.json").write_text('{"public":"index"}')
        (lazy / "owner-index.json").write_text(json.dumps({"version": 16, "courses": {"test-rail": self.full_descriptor}, "resources": {"test-rail": self.private_resources}}))
        (lazy / "owner-index.js").write_text("/* PRIVATE_INDEX_SENTINEL */")
        self.env = patch.dict(os.environ, {"COMMERCE_MODE": "protected", "BILLING_MODE": "disabled"})
        self.env.start()
        self.server = APP.ThreadingHTTPServer(("127.0.0.1", 0), APP.Handler)
        self.origin = f"http://127.0.0.1:{self.server.server_port}"
        self.app = APP.Application(self.root / "private/accounts.sqlite3", self.public, self.origin)
        self.server.app = self.app
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.password = "OwnerTest9!"  # test-only 10-character credential

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.env.stop()
        self.tmp.cleanup()

    def chunk(self, group, value, identifier="test-rail"):
        raw = json.dumps(value, ensure_ascii=False).encode()
        digest = hashlib.sha256(raw).hexdigest()
        name = f"data/lazy/{group}/{identifier}-{digest[:16]}.json"
        path = self.public / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        descriptor={"file": name, "script": name[:-5] + ".js", "sha256": digest, "byteLength": len(raw)}
        serialized=raw.decode().replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
        script='/* Generated on-demand data. */\nwindow.MG_LAZY_DATA=window.MG_LAZY_DATA||Object.create(null);\nwindow.MG_LAZY_DATA['+json.dumps(name)+']={sha256:'+json.dumps(digest)+',value:'+serialized+'};\n'
        (self.public/descriptor['script']).write_text(script)
        return descriptor

    def request(self, method, path, payload=None, cookie=""):
        client = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        headers = {"Origin": self.origin, "Content-Type": "application/json"}
        if cookie:
            headers["Cookie"] = cookie
        client.request(method, path, json.dumps(payload) if payload is not None else None, headers)
        response = client.getresponse()
        status, headers, body = response.status, dict(response.getheaders()), response.read()
        client.close()
        try:
            value = json.loads(body)
        except ValueError:
            value = body.decode()
        return status, headers, value

    def owner(self):
        record = verifier("kuonanhong", self.password)
        provision(self.app, record)
        status, headers, value = self.request("POST", "/api/login", {"login": "kuonanhong", "password": self.password})
        self.assertEqual(status, 200, value)
        self.assertTrue(value["user"]["owner"])
        self.assertIn("HttpOnly", headers["Set-Cookie"])
        return headers["Set-Cookie"].split(";", 1)[0], value["user"]

    def learner(self):
        status, headers, value = self.request("POST", "/api/register", {
            "username": "learner", "email": "learner@example.test", "phone": "+886911111111",
            "password": "Strong-test-password-only", "role": "owner", "owner": True})
        self.assertEqual(status, 200, value)
        self.assertFalse(value["user"]["owner"])
        return headers["Set-Cookie"].split(";", 1)[0], value["user"]

    def test_owner_full_access_without_payment_and_logout_discards_authority(self):
        cookie, user = self.owner()
        for path in ("/api/curriculum?courseId=test-rail", "/api/courses/test-rail"):
            status, headers, value = self.request("GET", path, cookie=cookie)
            self.assertEqual(status, 200)
            self.assertEqual(value["stages"][1]["steps"][0]["instruction"], "MEMBER_BODY_SENTINEL")
            self.assertIn("no-store", headers["Cache-Control"])
        account = self.request("GET", "/api/billing/me", cookie=cookie)[2]
        self.assertEqual((account["owner"], account["active"], account["accessType"]), (True, True, "owner"))
        self.assertEqual(account["orders"], [])
        self.assertEqual(account["entitlements"], [])
        self.assertEqual(self.request("POST", "/api/billing/checkout", {}, cookie)[0], 409)
        self.assertEqual(self.request("GET", "/api/me", cookie=cookie)[2]["user"]["id"], user["id"])
        self.assertEqual(self.request("POST", "/api/logout", {}, cookie)[0], 200)
        self.assertEqual(self.request("GET", "/api/billing/me", cookie=cookie)[0], 401)
        self.assertNotIn("MEMBER_BODY_SENTINEL", json.dumps(self.request("GET", "/api/courses/test-rail", cookie=cookie)[2]))

    def test_guest_and_registration_cannot_claim_owner_role_or_private_assets(self):
        cookie, _ = self.learner()
        self.assertFalse(self.request("GET", "/api/billing/me", cookie=cookie)[2]["active"])
        for auth in ("", cookie):
            value = self.request("GET", "/api/curriculum?courseId=test-rail", cookie=auth)[2]
            self.assertIn("FREE_FIRST_STAGE", json.dumps(value))
            self.assertNotIn("MEMBER_BODY_SENTINEL", json.dumps(value))
        reserved = {"username": "kuonanhong", "email": "other@example.test", "phone": "+886922222222", "password": "Another-strong-password"}
        self.assertEqual(self.request("POST", "/api/register", reserved)[0], 409)
        for path in ("/data/lazy/owner-index.json", "/data/lazy/owner-index.js", "/" + self.full_descriptor["file"], "/" + self.private_resources["file"]):
            self.assertEqual(self.request("GET", path, cookie=cookie)[0], 403, path)
        self.assertEqual(self.request("GET", "/api/curriculum?resources=../test-rail")[0], 400)

    def test_salted_verifier_and_reset_never_store_clear_password(self):
        first, second = verifier("kuonanhong", self.password), verifier("kuonanhong", self.password)
        self.assertNotEqual(first["salt"], second["salt"])
        self.assertNotIn(self.password, json.dumps(first))
        record_path = self.root / "owner-private/bootstrap.json"
        write_bootstrap(record_path, first)
        self.assertNotIn(self.password, record_path.read_text())
        if os.name != "nt":
            self.assertEqual(record_path.stat().st_mode & 0o777, 0o600)
        cookie, _ = self.owner()
        with self.assertRaises(ValueError):
            provision(self.app, second)
        provision(self.app, second, replace_existing=True)
        self.assertEqual(self.request("GET", "/api/billing/me", cookie=cookie)[0], 401)
        with self.app.db() as db:
            row = db.execute("SELECT salt,password_hash,role FROM users WHERE username='kuonanhong'").fetchone()
            self.assertEqual(len(row["salt"]), 32)
            self.assertEqual(len(row["password_hash"]), 32)
            self.assertEqual(row["role"], "owner")
            self.assertEqual(db.execute("SELECT count(*) FROM owner_admin_audit").fetchone()[0], 2)
        with self.assertRaises(ValueError):
            validate_verifier({**second, "rounds": 1})

    def test_initial_page_and_index_load_no_course_bodies_then_verify_one_chunk(self):
        self.assertEqual(len(self.app.commerce.full_courses), 0)
        self.assertEqual(self.request("GET", "/")[0], 200)
        self.assertEqual(self.request("GET", "/data/lazy/index.compact.json")[0], 200)
        index = self.request("GET", "/api/curriculum?index=1")[2]
        self.assertNotIn("MEMBER_BODY_SENTINEL", json.dumps(index))
        self.assertEqual(len(self.app.commerce.full_courses), 0)
        self.request("GET", "/api/courses/test-rail")
        self.assertEqual(list(self.app.commerce.full_courses), ["test-rail"])
        self.app.commerce.full_courses.clear()
        path = self.public / self.full_descriptor["file"]
        path.write_bytes(path.read_bytes().replace(b"MEMBER_BODY_SENTINEL", b"TAMPER_BODY_SENTINEL"))
        self.assertEqual(self.request("GET", "/api/courses/test-rail")[0], 503)

    def test_resource_authority_is_evaluated_per_request(self):
        cookie, _ = self.owner()
        owner_resources = self.request("GET", "/api/curriculum?resources=test-rail", cookie=cookie)
        self.assertEqual(owner_resources[0], 200)
        self.assertIn("MEMBER_GUIDE_SENTINEL", json.dumps(owner_resources[2]))
        guest_resources = self.request("GET", "/api/curriculum?resources=test-rail")
        self.assertEqual(guest_resources[0], 200)
        self.assertNotIn("MEMBER_GUIDE_SENTINEL", json.dumps(guest_resources[2]))
        self.request("POST", "/api/logout", {}, cookie)
        self.assertNotIn("MEMBER_GUIDE_SENTINEL", json.dumps(self.request("GET", "/api/curriculum?resources=test-rail", cookie=cookie)[2]))

    def test_member_pass_and_owner_completion_have_distinct_authority(self):
        member_cookie, member = self.learner()
        self.app.commerce.mode = "live"
        now = int(time.time())
        with self.app.db() as db:
            db.execute("INSERT INTO commerce_orders(id,user_id,plan_id,amount,duration_days,mode,status,created_at,trade_date,terms_version,request_key) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                       ("fixture-order", member["id"], "all-30", 299, 30, "live", "paid", now, "fixture", "fixture", "fixture"))
            db.execute("INSERT INTO commerce_entitlements VALUES(?,?,?,?,?,NULL)", ("fixture-order", member["id"], "live", now - 1, now + 3600))
        account = self.request("GET", "/api/billing/me", cookie=member_cookie)[2]
        self.assertFalse(account["owner"])
        self.assertTrue(account["active"])
        self.assertIn("MEMBER_BODY_SENTINEL", json.dumps(self.request("GET", "/api/courses/test-rail", cookie=member_cookie)[2]))
        owner_cookie, owner = self.owner()
        self.app.commerce.mode = "disabled"
        status = self.app.commerce.evidence_status(owner["id"], "test-rail")
        for step_id, answer in (("s1", 0), ("s2", 1)):
            self.assertTrue(self.app.commerce.evidence(owner["id"], {"courseId": "test-rail", "revision": status["revision"], "stepId": step_id, "answer": answer})["passed"])
        certificate = self.app.commerce.issue_certificate(owner, {"courseId": "test-rail"})
        self.assertTrue(certificate["valid"])
        self.assertEqual(certificate["steps"], 2)

    def test_v15_nested_guides_and_raw_media_never_bypass_api_authority(self):
        (self.public/'data/lazy/owner-index.json').unlink()
        full={'sources':[],'media':{'courses':[{'courseId':'test-rail','guides':[{'text':'MEMBER_GUIDE_SENTINEL'}]}]}}
        descriptor=self.chunk('resources',full)
        auxiliary=self.chunk('data',full['media'],'media')
        path=self.public/'data/lazy/index.json';index=json.loads(path.read_text())
        index['resources']['test-rail']=descriptor;index['auxiliary']={'media':auxiliary};path.write_text(json.dumps(index))
        (self.public/'data/media.json').write_text(json.dumps(full['media']))
        response=self.request('GET','/api/curriculum?resources=test-rail')
        self.assertEqual(response[0],200)
        self.assertNotIn('MEMBER_GUIDE_SENTINEL',json.dumps(response[2]))
        for name in ('data/media.json',descriptor['file'],descriptor['script'],auxiliary['file'],auxiliary['script']):
            self.assertEqual(self.request('GET','/'+name)[0],403,name)

    def test_public_scene_descriptor_works_but_unlisted_and_stale_scripts_fail(self):
        descriptor=self.chunk('data',{'version':16,'photos':[]},'scene-photos-v16')
        path=self.public/'data/lazy/index.json';index=json.loads(path.read_text())
        index['auxiliary']={'scene-photos-v16':descriptor};path.write_text(json.dumps(index))
        for name in (descriptor['file'],descriptor['script'],self.public_resources['file'],self.public_resources['script'],self.public_descriptor['file'],self.public_descriptor['script']):
            self.assertEqual(self.request('GET','/'+name)[0],200,name)
        stale=self.chunk('data',{'private':'MEMBER_GUIDE_SENTINEL'},'scene-photos-v16')
        self.assertEqual(self.request('GET','/'+stale['file'])[0],403)
        (self.public/descriptor['script']).write_text('window.secret="MEMBER_GUIDE_SENTINEL";')
        self.assertEqual(self.request('GET','/'+descriptor['script'])[0],403)

    def test_directory_index_symlink_cannot_escape_public_root(self):
        secret=self.root/'private-secret.txt';secret.write_text('PRIVATE_ROOT_ESCAPE_SENTINEL')
        index=self.public/'index.html';index.unlink()
        try:index.symlink_to(secret)
        except OSError:self.skipTest('Symlinks unavailable')
        for path in ('/','/index.html','//'):
            status,_,value=self.request('GET',path)
            self.assertEqual(status,404)
            self.assertNotIn('PRIVATE_ROOT_ESCAPE_SENTINEL',str(value))

    def test_launcher_enforces_protection_even_with_old_demo_environment(self):
        import sys
        from portable import launch_v16
        with patch.dict(os.environ,{'COMMERCE_MODE':'demo'}),patch.object(launch_v16,'ROOT',self.root),patch.object(launch_v16,'read_dotenv'),patch.object(launch_v16,'serve') as serve,patch.object(sys,'argv',['launch_v16.py']):
            launch_v16.main()
            self.assertEqual(os.environ['COMMERCE_MODE'],'protected')
            serve.assert_called_once()


if __name__ == "__main__":
    unittest.main()
