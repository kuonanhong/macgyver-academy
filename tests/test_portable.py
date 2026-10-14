"""Run: python3 -m unittest discover -s tests -p 'test_*.py' -v"""
import http.client
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from portable import server as APP


class PortableSecurityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        public = root / "public"
        public.mkdir()
        (public / "index.html").write_text("<!doctype html><title>Test</title>")
        (root / "private.txt").write_text("private")
        self.server = APP.ThreadingHTTPServer(("127.0.0.1", 0), APP.Handler)
        self.port = self.server.server_port
        self.origin = f"http://127.0.0.1:{self.port}"
        self.server.app = APP.Application(root / "data/accounts.sqlite3", public, self.origin)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()

    def request(self, method, path, data=None, cookie="", origin=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        request_headers = {"Content-Type": "application/json", "Origin": origin or self.origin}
        if cookie:
            request_headers["Cookie"] = cookie
        request_headers.update(headers or {})
        connection.request(method, path, body=json.dumps(data) if data is not None else None, headers=request_headers)
        response = connection.getresponse()
        status, output_headers, raw = response.status, dict(response.getheaders()), response.read()
        connection.close()
        try:
            value = json.loads(raw)
        except ValueError:
            value = raw.decode()
        return status, output_headers, value

    def register(self, email):
        status, headers, value = self.request("POST", "/api/register", {"email": email, "name": "工程學徒", "password": "Strong-learning-passphrase-123"})
        self.assertEqual(status, 200, value)
        self.assertIn("HttpOnly", headers["Set-Cookie"])
        self.assertIn("SameSite=Lax", headers["Set-Cookie"])
        return headers["Set-Cookie"].split(";", 1)[0], value["user"]

    def test_accounts_are_isolated_and_logout_revokes_session(self):
        first, user_a = self.register("a@example.test")
        status, _, _ = self.request("PUT", "/api/progress", {"projectId": "project-1", "completed": ["step-1"], "notes": "精度驗證", "assembly": ["optics"]}, first)
        self.assertEqual(status, 200)
        second, user_b = self.register("b@example.test")
        self.assertNotEqual(user_a["id"], user_b["id"])
        self.assertEqual(self.request("GET", "/api/progress", cookie=second)[2], {"projects": {}})
        first_progress = self.request("GET", "/api/progress", cookie=first)[2]
        self.assertEqual(first_progress["projects"]["project-1"]["notes"], "精度驗證")
        self.assertEqual(self.request("POST", "/api/logout", {}, first)[0], 200)
        self.assertEqual(self.request("GET", "/api/progress", cookie=first)[0], 401)
        # Signing in again recovers the same account and durable progress.
        status, headers, data = self.request("POST", "/api/login", {"email": "A@EXAMPLE.TEST", "password": "Strong-learning-passphrase-123"})
        self.assertEqual(status, 200)
        self.assertEqual(data["user"]["id"], user_a["id"])
        self.assertIn("project-1", self.request("GET", "/api/progress", cookie=headers["Set-Cookie"].split(";", 1)[0])[2]["projects"])

    def test_stale_tab_cannot_save_to_a_new_cookie_owner(self):
        cookie_a, user_a = self.register("alice@example.test")
        cookie_b, user_b = self.register("bob@example.test")
        payload = {"projectId": "project-1", "ownerId": user_b["id"], "completed": [], "assembly": [], "notes": "Bob private notes", "baseUpdatedAt": None}
        self.assertEqual(self.request("PUT", "/api/progress", payload, cookie_a)[0], 409)
        self.assertEqual(self.request("GET", "/api/progress", cookie=cookie_a)[2], {"projects": {}})
        self.assertEqual(self.request("PUT", "/api/progress", payload, cookie_b)[0], 200)
        self.assertEqual(self.request("GET", "/api/progress", cookie=cookie_b)[2]["projects"]["project-1"]["notes"], "Bob private notes")

    def test_authentication_origin_validation_and_unavailable_ai(self):
        self.assertEqual(self.request("GET", "/api/progress", headers={"oai-authenticated-user-id": "forged", "oai-authenticated-user-email": "attacker@example.test"})[0], 401)
        self.assertEqual(self.request("POST", "/api/register", {"email": "short@example.test", "name": "Short", "password": "short"})[0], 400)
        cookie, _ = self.register("learner@example.test")
        payload = {"projectId": "project-1", "completed": [], "notes": "", "assembly": []}
        self.assertEqual(self.request("PUT", "/api/progress", payload, cookie, "https://attacker.test")[0], 403)
        self.assertEqual(self.request("PUT", "/api/progress", {**payload, "projectId": "../../private"}, cookie)[0], 400)
        self.assertEqual(self.request("PUT", "/api/progress", {**payload, "completed": ["<script>"]}, cookie)[0], 400)
        with patch.dict(os.environ, {"AI_BASE_URL": "", "AI_MODEL": "", "AI_API_KEY": ""}):
            self.assertFalse(self.request("GET", "/api/me", cookie=cookie)[2]["aiAvailable"])
            self.assertEqual(self.request("POST", "/api/tutor", {"question": "什麼是熱應力？"}, cookie)[0], 503)
            self.assertEqual(self.request("POST", "/api/translate", {"texts": ["thermal stress"], "language": "zh-TW"}, cookie)[0], 503)
        self.assertEqual(self.request("GET", "/../private.txt")[0], 404)
        self.assertEqual(self.request("GET", "/%2e%2e/private.txt")[0], 404)
        self.assertEqual(self.request("GET", "/")[0], 200)
        self.assertEqual(self.request("GET", "/api/me", headers={"Host": "attacker.test"})[0], 403)

    def test_generated_answers_use_real_adapter_and_rate_limits(self):
        cookie, user = self.register("ai@example.test")
        with patch.dict(os.environ, {"AI_BASE_URL": "https://model.example/v1", "AI_MODEL": "configured-model", "AI_API_KEY": "test-only"}):
            with patch.object(APP, "ai_completion", return_value="Thermal stress depends on expansion mismatch.") as adapter:
                status, _, result = self.request("POST", "/api/tutor", {"question": "Explain thermal stress.", "context": "Source: course handout", "language": "en", "cloudConsent": True}, cookie)
                self.assertEqual(status, 200)
                self.assertTrue(result["generated"])
                self.assertEqual(result["model"], "configured-model")
                self.assertEqual(adapter.call_args[0][1]["reference_context"], "Source: course handout")
            with self.server.app.db() as db:
                db.execute("UPDATE ai_rate_limits SET count=60 WHERE user_id=?", (user["id"],))
            self.assertEqual(self.request("POST", "/api/tutor", {"question": "Another question", "cloudConsent": True}, cookie)[0], 429)

    def test_concurrent_updates_return_current_version_without_overwrite(self):
        cookie, _ = self.register("concurrency@example.test")
        payload = {"projectId": "project-1", "completed": ["step-1"], "assembly": ["part-1"], "notes": "first", "baseUpdatedAt": None}
        status, _, first = self.request("PUT", "/api/progress", payload, cookie)
        self.assertEqual(status, 200)
        status, _, second = self.request("PUT", "/api/progress", {**payload, "notes": "device A", "baseUpdatedAt": first["updatedAt"]}, cookie)
        self.assertEqual(status, 200)
        self.assertGreater(second["updatedAt"], first["updatedAt"])
        status, _, conflict = self.request("PUT", "/api/progress", {**payload, "notes": "device B", "baseUpdatedAt": first["updatedAt"]}, cookie)
        self.assertEqual(status, 409)
        self.assertEqual(conflict["current"]["notes"], "device A")
        self.assertEqual(conflict["current"]["updatedAt"], second["updatedAt"])
        self.assertEqual(self.request("GET", "/api/progress", cookie=cookie)[2]["projects"]["project-1"]["notes"], "device A")
        status, _, merged = self.request("PUT", "/api/progress", {**payload, "notes": "device A\n[Conflict]\ndevice B", "completed": ["step-1", "step-2"], "baseUpdatedAt": conflict["current"]["updatedAt"]}, cookie)
        self.assertEqual(status, 200)
        self.assertEqual(len(merged["completed"]), 2)
        # Omitting the base cannot silently overwrite an existing record.
        self.assertEqual(self.request("PUT", "/api/progress", payload, cookie)[0], 409)


if __name__ == "__main__":
    unittest.main()
