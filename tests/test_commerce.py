"""Deterministic commerce security tests; no provider calls or real payments."""
import copy
import http.client
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from urllib.parse import urlencode

from portable import server as APP
from portable.commerce import Commerce, TERMS_VERSION, check_mac, parse_notification


class CommerceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.public = root / "public"
        (self.public / "data/course-parts").mkdir(parents=True)
        self.course = {"id": "paid-course", "title": "Paid", "titleEn": "Paid course", "summary": "Public summary", "category": "electronics", "stepCount": 2, "stages": [{"id": "stage1", "steps": [{"id": "s1", "objective": "Private first lesson", "quiz": {"answer": 1}}, {"id": "s2", "objective": "Private second lesson", "quiz": {"answer": 0}}]}]}
        self.free = {**copy.deepcopy(self.course), "id": "semiconductor"}
        (self.public / "data/featured.json").write_text(json.dumps([self.course, self.free]))
        (self.public / "data/catalog.json").write_text('[{"id":"paid-course","title":"Public"}]')
        (self.public / "data/course-parts/part-0001-test.json").write_text("private")
        (self.public / "offline-data-01.js").write_text("private full course")
        (self.public / "full-source.zip").write_bytes(b"private full source")
        (self.public / "index.html").write_text("<!doctype html><title>Demo</title>")
        (self.public / "app.js").write_text("/* public application */")
        (self.public / "alias.js").symlink_to(self.public / "data/featured.json")
        self.environment = patch.dict(os.environ, {"COMMERCE_MODE": "protected", "BILLING_MODE": "live", "ECPAY_MERCHANT_ID": "9000001", "ECPAY_HASH_KEY": "test-key-only-000", "ECPAY_HASH_IV": "test-iv-only-0000", "ECPAY_LIVE_CONFIRMED": "1", "COMMERCE_LEGAL_READY": "1"})
        self.environment.start()
        self.server = APP.ThreadingHTTPServer(("127.0.0.1", 0), APP.Handler)
        self.origin = "https://academy.example.test"
        self.server.app = APP.Application(root / "accounts.sqlite3", self.public, self.origin)
        self.billing = self.server.app.commerce
        self.provider = patch.object(self.billing, "query_transport", side_effect=self.provider_response)
        self.provider.start()
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        with self.server.app.db() as db:
            for uid in ("alice", "bob"):
                db.execute("INSERT INTO users VALUES(?,?,?,?,?,?)", (uid, uid + "@example.test", "學徒 " + uid, b"salt", b"hash", 0))
            import hashlib
            self.token = "A" * 64
            db.execute("INSERT INTO sessions VALUES(?,?,?)", (hashlib.sha256(self.token.encode()).hexdigest(), "alice", int(time.time()) + 10000))

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.provider.stop()
        self.environment.stop()
        self.tmp.cleanup()

    def request(self, method, path, value=None, auth=False, raw=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        request_headers = {"Host": "academy.example.test", "Origin": self.origin, "Content-Type": "application/json"}
        if auth:
            request_headers["Cookie"] = APP.COOKIE + "=" + self.token
        request_headers.update(headers or {})
        conn.request(method, path, body=raw if raw is not None else json.dumps(value) if value is not None else None, headers=request_headers)
        response = conn.getresponse()
        status, out_headers, body = response.status, dict(response.getheaders()), response.read()
        conn.close()
        try:
            body = json.loads(body)
        except ValueError:
            body = body.decode()
        return status, out_headers, body

    def checkout(self, user="alice", request_id="unique-request-0001"):
        return self.billing.checkout(user, {"planId": "all-30", "termsAccepted": True, "termsVersion": TERMS_VERSION, "requestId": request_id})

    def notification(self, checkout, **overrides):
        fields = {"MerchantID": self.billing.merchant, "MerchantTradeNo": checkout["orderId"], "TradeAmt": "299", "TradeNo": "PAY" + checkout["orderId"][2:18], "RtnCode": "1", "SimulatePaid": "0", "PaymentType": "Credit_CreditCard", "PaymentDate": "2026/10/14 10:00:00"}
        fields.update(overrides)
        fields["CheckMacValue"] = check_mac(fields, self.billing.key, self.billing.iv)
        return urlencode(fields).encode()

    def provider_response(self, url, body):
        query = parse_notification(body, APP.ApiError)
        order = {"orderId": query["MerchantTradeNo"]}
        fields = parse_notification(self.notification(order), APP.ApiError)
        fields.pop("RtnCode")
        fields.pop("SimulatePaid")
        fields["TradeStatus"] = "1"
        fields["CheckMacValue"] = check_mac(fields, self.billing.key, self.billing.iv)
        return urlencode(fields).encode()

    def assert_error(self, status, callback):
        with self.assertRaises(APP.ApiError) as raised:
            callback()
        self.assertEqual(raised.exception.status, status, raised.exception.message)

    def test_official_ecpay_test_vector(self):
        fields = dict(pair.split("=", 1) for pair in "TradeDesc=促銷方案&PaymentType=aio&MerchantTradeDate=2023/03/12 15:30:23&MerchantTradeNo=ecpay20230312153023&MerchantID=3002607&ReturnURL=https://www.ecpay.com.tw/receive.php&ItemName=Apple iphone 15&TotalAmount=30000&ChoosePayment=ALL&EncryptType=1".split("&"))
        self.assertEqual(check_mac(fields, "pwFHCqoQZGmho4w6", "EkRm7iFT261dpevs"), "6C51C9E6888DE861FD62FB1DD17029FC742634498FD813DC43D4243B5685B840")

    def test_default_configuration_does_not_enable_checkout(self):
        with patch.dict(os.environ, {"COMMERCE_MODE": "demo", "BILLING_MODE": "disabled"}):
            default = Commerce(self.server.app, APP.ApiError)
        self.assertFalse(default.config()["checkoutAvailable"])
        self.assertFalse(default.protected)
        self.assert_error(503, lambda: default.checkout("alice", {}))
        self.assertNotIn(self.billing.key, json.dumps(default.config()))

    def test_live_needs_explicit_flags_public_https_and_non_test_merchant(self):
        for key, value in (("ECPAY_LIVE_CONFIRMED", ""), ("COMMERCE_LEGAL_READY", ""), ("ECPAY_MERCHANT_ID", "3002607"), ("ECPAY_HASH_KEY", "")):
            with self.subTest(key=key), patch.dict(os.environ, {key: value}):
                self.assertFalse(Commerce(self.server.app, APP.ApiError).available)
        original = self.server.app.origin
        self.server.app.origin = "http://localhost:8010"
        self.assertFalse(Commerce(self.server.app, APP.ApiError).available)
        self.server.app.origin = original

    def test_checkout_amount_is_server_owned_and_request_is_idempotent(self):
        result = self.checkout()
        self.assertEqual(result["fields"]["TotalAmount"], "299")
        self.assertEqual(result["orderId"], self.checkout()["orderId"])
        self.assertEqual(len(result["orderId"]), 20)
        self.assertNotIn(self.billing.key, json.dumps(result))
        self.assertNotIn(self.billing.iv, json.dumps(result))
        self.assertEqual(result["action"], "https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5")
        self.assert_error(400, lambda: self.billing.checkout("alice", {"planId": "all-30", "amount": 1}))

    def test_invalid_signatures_amounts_merchants_and_duplicate_fields_grant_nothing(self):
        order = self.checkout()
        valid = self.notification(order)
        self.assert_error(400, lambda: self.billing.notification(valid.replace(b"TradeAmt=299", b"TradeAmt=1")))
        for changes in ({"TradeAmt": "1"}, {"MerchantID": "9000002"}, {"TradeAmt": "299.0"}, {"MerchantTradeNo": "MG" + "0" * 18}):
            self.assert_error(400, lambda: self.billing.notification(self.notification(order, **changes)))
        self.assert_error(400, lambda: self.billing.notification(valid + b"&TradeAmt=299"))
        self.assertFalse(self.billing.entitlement("alice"))

    def test_failed_and_simulated_payment_do_not_grant_access(self):
        order = self.checkout()
        self.assertEqual(self.billing.notification(self.notification(order, RtnCode="10100248")), "1|OK")
        self.assertEqual(self.billing.notification(self.notification(order, SimulatePaid="1")), "1|OK")
        self.assertFalse(self.billing.entitlement("alice"))
        with self.server.app.db() as db:
            self.assertEqual(db.execute("SELECT status FROM commerce_orders").fetchone()[0], "pending")

    def test_paid_notification_is_atomic_idempotent_and_account_scoped(self):
        order = self.checkout()
        raw = self.notification(order)
        self.assertEqual(self.billing.notification(raw), "1|OK")
        before = self.billing.entitlement("alice")
        self.assertEqual(self.billing.notification(raw), "1|OK")
        self.assertEqual(self.billing.entitlement("alice"), before)
        self.assertFalse(self.billing.entitlement("bob"))
        self.assertEqual(before["expires_at"] - before["starts_at"], 30 * 86400)
        self.billing.notification(self.notification(order, RtnCode="10100248"))
        self.assertTrue(self.billing.entitlement("alice"))

    def test_reused_provider_trade_is_rejected(self):
        first = self.checkout()
        raw = self.notification(first)
        self.billing.notification(raw)
        second = self.checkout("bob", "unique-request-bob01")
        trade = parse_notification(raw, APP.ApiError)["TradeNo"]
        self.assert_error(503, lambda: self.billing.notification(self.notification(second, TradeNo=trade)))
        self.assertFalse(self.billing.entitlement("bob"))

    def test_provider_query_failure_tampering_or_pending_never_grants(self):
        order = self.checkout()
        raw = self.notification(order)
        with patch.object(self.billing, "query_transport", return_value=b"MerchantID=9000001&CheckMacValue=bad"):
            self.assert_error(502, lambda: self.billing.notification(raw))
        with patch.object(self.billing, "query_order", return_value={"TradeStatus": "0"}):
            self.assert_error(503, lambda: self.billing.notification(raw))
        self.assertFalse(self.billing.entitlement("alice"))

    def test_admin_reconcile_recovers_missing_notification_without_client_success(self):
        order = self.checkout()
        self.assertFalse(self.billing.entitlement("alice"))
        self.assertTrue(self.billing.reconcile(order["orderId"])["granted"])
        self.assertTrue(self.billing.entitlement("alice"))

    def test_sandbox_entitlement_cannot_open_live_courses(self):
        self.billing.mode = "sandbox"
        order = self.checkout()
        self.assertIn("payment-stage", order["action"])
        self.billing.notification(self.notification(order))
        self.assertTrue(self.billing.can_access("paid-course", "alice"))
        self.billing.mode = "live"
        self.assertFalse(self.billing.can_access("paid-course", "alice"))

    def test_expiry_and_revocation_are_enforced_and_webhook_cannot_restore(self):
        order = self.checkout()
        self.billing.notification(self.notification(order))
        with self.server.app.db() as db:
            db.execute("UPDATE commerce_entitlements SET expires_at=?", (int(time.time()) - 1,))
        self.assertFalse(self.billing.can_access("paid-course", "alice"))
        self.billing.revoke_order(order["orderId"], "Refund confirmed in provider dashboard")
        self.billing.notification(self.notification(order, PaymentDate="2026/10/15 11:00:00"))
        self.assertFalse(self.billing.can_access("paid-course", "alice"))

    def test_curriculum_does_not_disclose_paid_steps_and_static_bypasses_fail(self):
        status, _, result = self.request("GET", "/api/curriculum")
        self.assertEqual(status, 200)
        paid = next(c for c in result if c["id"] == "paid-course")
        self.assertTrue(paid["locked"])
        self.assertEqual(paid["stages"], [])
        self.assertNotIn("Private first lesson", json.dumps(paid))
        self.assertTrue(next(c for c in result if c["id"] == "semiconductor")["stages"])
        for path in ("/data/featured.json", "/data/course-parts/part-0001-test.json", "/offline-data-01.js", "/alias.js", "/full-source.zip", "/data/../offline-data-01.js", "/%6fffline-data-01.js"):
            self.assertEqual(self.request("GET", path, auth=True, headers={"Range": "bytes=0-100"})[0], 403, path)
        self.assertEqual(self.request("GET", "/app.js")[0], 200)
        self.assertEqual(self.request("GET", "/data/catalog.json")[0], 200)
        self.assertEqual(self.request("GET", "/api/courses/paid-course", auth=True)[0], 402)
        self.assertEqual(self.request("GET", "/api/courses/semiconductor")[0], 200)

    def test_unauthorized_paid_progress_and_cross_origin_checkout_fail(self):
        payload = {"projectId": "paid-course", "completed": ["s1", "s2"], "assembly": [], "notes": "", "baseUpdatedAt": None}
        self.assertEqual(self.request("PUT", "/api/progress", payload, auth=True)[0], 402)
        self.assertEqual(self.request("POST", "/api/billing/checkout", {}, auth=True, headers={"Origin": "https://attacker.test"})[0], 403)
        self.assertEqual(self.request("POST", "/api/billing/checkout", {})[0], 401)
        self.assertEqual(self.request("POST", "/api/certificates", {"courseId": "semiconductor", "expectedUserId": "bob"}, auth=True)[0], 409)

    def test_public_market_route_uses_fixed_vendor_parameter(self):
        with patch.object(APP, "market_quote", return_value={"status": "unconfigured", "symbol": "TEST"}) as mocked:
            status, headers, result = self.request("GET", "/api/markets?vendor=demo")
            self.assertEqual(status, 200)
            self.assertEqual(result["symbol"], "TEST")
            mocked.assert_called_once_with("demo")
            self.assertIn("no-store", headers["Cache-Control"])
        for path in ("/api/markets", "/api/markets?vendor=no-such-issuer", "/api/markets?vendor=a&vendor=b", "/api/markets?vendor=a&url=https://attacker.test"):
            self.assertEqual(self.request("GET", path)[0], 400, path)

    def test_free_evidence_survives_live_activation_but_sandbox_does_not(self):
        self.billing.mode = "disabled"
        state = self.billing.evidence_status("alice", "semiconductor")
        self.billing.evidence("alice", {"courseId": "semiconductor", "revision": state["revision"], "stepId": "s1", "answer": 1})
        self.billing.mode = "live"
        self.assertEqual(self.billing.evidence_status("alice", "semiconductor")["completed"], ["s1"])
        self.billing.mode = "sandbox"
        self.assertEqual(self.billing.evidence_status("alice", "semiconductor")["completed"], [])

    def test_callback_does_not_require_browser_cookie_or_origin(self):
        order = self.checkout()
        status, headers, result = self.request("POST", "/api/billing/ecpay/notify", raw=self.notification(order), headers={"Content-Type": "application/x-www-form-urlencoded", "Origin": "https://provider.example"})
        self.assertEqual((status, result), (200, "1|OK"))
        self.assertTrue(headers["Content-Type"].startswith("text/plain"))
        self.assertEqual(self.request("GET", "/api/billing/me")[0], 401)

    def test_certificate_rejects_client_progress_skips_wrong_answers_and_stale_revision(self):
        status = self.billing.evidence_status("alice", "semiconductor")
        self.assert_error(409, lambda: self.billing.issue_certificate({"id": "alice", "name": "Learner"}, {"courseId": "semiconductor", "completed": ["s1", "s2"]}))
        base = {"courseId": "semiconductor", "revision": status["revision"], "stepId": "s2", "answer": 0}
        self.assert_error(409, lambda: self.billing.evidence("alice", base))
        self.assert_error(409, lambda: self.billing.evidence("alice", {**base, "revision": "forged"}))
        wrong = self.billing.evidence("alice", {**base, "stepId": "s1", "answer": 0})
        self.assertFalse(wrong["passed"])
        self.assertEqual(self.billing.evidence_status("alice", "semiconductor")["completed"], [])

    def test_certificate_is_verifiable_private_and_not_cross_account(self):
        state = self.billing.evidence_status("alice", "semiconductor")
        for step, answer in (("s1", 1), ("s2", 0)):
            self.billing.evidence("alice", {"courseId": "semiconductor", "revision": state["revision"], "stepId": step, "answer": answer})
        certificate = self.billing.issue_certificate({"id": "alice", "name": "Private name"}, {"courseId": "semiconductor"})
        self.assertTrue(certificate["valid"])
        self.assertEqual(certificate["displayName"], "Learner")
        self.assertNotIn("alice", json.dumps(certificate))
        self.assertNotIn("email", certificate)
        self.assertEqual(self.billing.verify_certificate(certificate["id"]), certificate)
        self.assertEqual(self.request("GET", "/api/certificates/" + certificate["id"])[0], 200)
        rendered = self.request("GET", "/api/certificates/" + certificate["id"], headers={"Accept": "text/html"})
        self.assertEqual(rendered[0], 200)
        self.assertIn("text/html", rendered[1]["Content-Type"])
        self.assertIn("Certificate of Course Completion", rendered[2])
        self.assertIn("window.print()", rendered[2])
        self.assertNotIn("Private name", rendered[2])
        self.assert_error(409, lambda: self.billing.issue_certificate({"id": "bob", "name": "Bob"}, {"courseId": "semiconductor"}))
        self.assert_error(404, lambda: self.billing.verify_certificate("a" * 40))

    def test_revoking_paid_order_revokes_its_certificate(self):
        order = self.checkout()
        self.billing.notification(self.notification(order))
        state = self.billing.evidence_status("alice", "paid-course")
        for step, answer in (("s1", 1), ("s2", 0)):
            self.billing.evidence("alice", {"courseId": "paid-course", "revision": state["revision"], "stepId": step, "answer": answer})
        certificate = self.billing.issue_certificate({"id": "alice", "name": "Alice"}, {"courseId": "paid-course"})
        result = self.billing.revoke_order(order["orderId"], "Provider refund has been confirmed")
        self.assertFalse(result["moneyRefunded"])
        self.assertFalse(self.billing.verify_certificate(certificate["id"])["valid"])


if __name__ == "__main__":
    unittest.main()
