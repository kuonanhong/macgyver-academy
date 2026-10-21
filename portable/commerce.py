"""Optional same-origin ECPay commerce and server-recorded learning evidence.

Standard library only. Defaults to disabled. The author/source distribution is
not a paywall: a protected deployment must serve every path through server.py.
"""
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import html
import json
import os
import re
import secrets
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, quote_plus, urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

TERMS_VERSION = "v10-2026-10"
# V12: no course is entirely free; the first stage of every course is.
FREE_COURSES = ()
FREE_STAGES = int(os.environ.get("FREE_STAGES_PER_COURSE", "1"))
PLANS = (
    {"id": "all-30", "title": "全學院 30 天", "titleEn": "Academy · 30 days", "amountTwd": 299, "durationDays": 30},
    {"id": "all-365", "title": "全學院 365 天", "titleEn": "Academy · 365 days", "amountTwd": 2490, "durationDays": 365},
)
SCHEMA = """
CREATE TABLE IF NOT EXISTS commerce_orders (
 id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id), plan_id TEXT NOT NULL,
 amount INTEGER NOT NULL, duration_days INTEGER NOT NULL, mode TEXT NOT NULL,
 status TEXT NOT NULL, created_at INTEGER NOT NULL, trade_date TEXT NOT NULL,
 terms_version TEXT NOT NULL, request_key TEXT NOT NULL,
 provider_trade TEXT UNIQUE, paid_at INTEGER, last_code TEXT,
 UNIQUE(user_id, request_key)
);
CREATE TABLE IF NOT EXISTS commerce_events (
 digest TEXT PRIMARY KEY, order_id TEXT NOT NULL, event_at INTEGER NOT NULL,
 result TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS commerce_entitlements (
 order_id TEXT PRIMARY KEY REFERENCES commerce_orders(id), user_id TEXT NOT NULL,
 mode TEXT NOT NULL, starts_at INTEGER NOT NULL, expires_at INTEGER NOT NULL,
 revoked_at INTEGER
);
CREATE INDEX IF NOT EXISTS commerce_entitlements_user ON commerce_entitlements(user_id,mode,expires_at);
CREATE TABLE IF NOT EXISTS learning_evidence (
 user_id TEXT NOT NULL REFERENCES users(id), course_id TEXT NOT NULL,
 revision TEXT NOT NULL, step_id TEXT NOT NULL, passed_at INTEGER NOT NULL,
 mode TEXT NOT NULL, PRIMARY KEY(user_id,course_id,revision,step_id,mode)
);
CREATE TABLE IF NOT EXISTS evidence_attempts (
 user_id TEXT NOT NULL, hour INTEGER NOT NULL, count INTEGER NOT NULL,
 PRIMARY KEY(user_id,hour)
);
CREATE TABLE IF NOT EXISTS learning_certificates (
 id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id), course_id TEXT NOT NULL,
 revision TEXT NOT NULL, course_title TEXT NOT NULL, course_title_en TEXT NOT NULL,
 step_count INTEGER NOT NULL, public_name TEXT NOT NULL, issued_at INTEGER NOT NULL,
 mode TEXT NOT NULL, order_id TEXT, revoked_at INTEGER,
 UNIQUE(user_id,course_id,revision,mode)
);
CREATE TABLE IF NOT EXISTS commerce_admin_audit (
 id INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT NOT NULL,
 action TEXT NOT NULL, reason TEXT NOT NULL, at INTEGER NOT NULL
);
"""


def check_mac(fields, key, iv):
    """ECPay AIO SHA-256/.NET encoding; excludes only CheckMacValue."""
    raw = "&".join(f"{k}={fields[k]}" for k in sorted(fields, key=str.lower) if k != "CheckMacValue")
    encoded = quote_plus(f"HashKey={key}&{raw}&HashIV={iv}", safe="-_.!*()")
    # Python always leaves '~' unescaped; .NET/ECPay encodes it.
    encoded = encoded.replace("~", "%7e").lower()
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest().upper()


def parse_notification(raw, error):
    try:
        if len(raw) > 32768:
            raise ValueError()
        pairs = parse_qsl(raw.decode("utf-8", errors="strict"), keep_blank_values=True,
                          strict_parsing=True, max_num_fields=100, errors="strict")
        fields = dict(pairs)
        if not fields or len(fields) != len(pairs) or any(not re.fullmatch(r"[A-Za-z][A-Za-z0-9]{0,60}", k) or len(v) > 2000 for k, v in pairs):
            raise ValueError()
        return fields
    except (ValueError, UnicodeError):
        raise error(400, "Invalid payment notification.") from None


def revision(course):
    return hashlib.sha256(json.dumps(course, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def steps(course):
    return [s for stage in course.get("stages", []) for s in stage.get("steps", [])]


class NoPaymentRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Commerce:
    def __init__(self, app, error):
        self.app, self.error = app, error
        self.mode = os.environ.get("BILLING_MODE", "disabled")
        self.protected = os.environ.get("COMMERCE_MODE", "demo") == "protected"
        if self.mode not in ("disabled", "sandbox", "live"):
            raise ValueError("BILLING_MODE must be disabled, sandbox or live.")
        if os.environ.get("COMMERCE_MODE", "demo") not in ("demo", "protected"):
            raise ValueError("COMMERCE_MODE must be demo or protected.")
        self.merchant = os.environ.get("ECPAY_MERCHANT_ID", "")
        self.key = os.environ.get("ECPAY_HASH_KEY", "")
        self.iv = os.environ.get("ECPAY_HASH_IV", "")
        self.courses = None
        self.revisions = {}
        self.reason = "Billing is disabled. This is the complete owner/demo edition."
        if self.protected:
            self.reason = "Paid access is protected; checkout is not configured."
            source = app.public / "data/featured.json"
            if not source.is_file():
                raise ValueError("Protected deployment requires the private canonical data/featured.json.")
            self.courses = {c["id"]: c for c in json.loads(source.read_text(encoding="utf-8"))}
        origin = urlsplit(app.origin)
        https_public = origin.scheme == "https" and origin.hostname not in ("localhost", "127.0.0.1", "::1") and origin.port in (None, 443)
        configured = bool(re.fullmatch(r"[0-9]{5,10}", self.merchant) and len(self.key) >= 16 and len(self.iv) >= 16)
        self.available = self.protected and self.mode != "disabled" and configured and https_public
        if self.mode == "live":
            self.available = self.available and self.merchant not in ("2000132", "3002607", "3002599", "3365120") and os.environ.get("ECPAY_LIVE_CONFIRMED") == "1" and os.environ.get("COMMERCE_LEGAL_READY") == "1"
        if self.available:
            self.reason = "Sandbox only: no real payment or production entitlement." if self.mode == "sandbox" else "Hosted card checkout. No automatic renewal."
        with app.db() as db:
            db.executescript(SCHEMA)

    def config(self):
        return {"mode": self.mode, "protected": self.protected, "checkoutAvailable": bool(self.available),
                "freeCourseIds": list(FREE_COURSES), "freeStagesPerCourse": FREE_STAGES, "plans": list(PLANS), "termsVersion": TERMS_VERSION,
                "termsUrl": "/commerce-terms.html", "reason": self.reason,
                "legalUrls": {"terms": self.app.origin + "/commerce-terms.html", "privacy": self.app.origin + "/commerce-terms.html#privacy", "refund": self.app.origin + "/commerce-terms.html#refund"},
                "certificateType": "server-recorded-quiz-completion" if self.protected else "local-learning-statement"}

    def load_courses(self):
        if self.courses is None:
            path = self.app.public / "data/featured.json"
            if not path.is_file():
                raise self.error(503, "Curriculum is not configured.")
            self.courses = {c["id"]: c for c in json.loads(path.read_text(encoding="utf-8"))}
        return self.courses

    def course(self, course_id):
        if not isinstance(course_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,100}", course_id):
            raise self.error(400, "Invalid course ID.")
        course = self.load_courses().get(course_id)
        if not course:
            raise self.error(404, "Guided course not found.")
        return course

    def course_revision(self, course):
        if course["id"] not in self.revisions:
            self.revisions[course["id"]] = revision(course)
        return self.revisions[course["id"]]

    def entitlement(self, user_id, db=None):
        if not user_id or self.mode not in ("live", "sandbox"):
            return None
        if db is None:
            with self.app.db() as connection:
                return self.entitlement(user_id, connection)
        now = int(time.time())
        row = db.execute("SELECT * FROM commerce_entitlements WHERE user_id=? AND mode=? AND revoked_at IS NULL AND starts_at<=? AND expires_at>? ORDER BY expires_at DESC LIMIT 1", (user_id, self.mode, now, now)).fetchone()
        return dict(row) if row else None

    def can_access(self, course_id, user_id):
        return not self.protected or course_id in FREE_COURSES or bool(self.entitlement(user_id))

    def require_access(self, course_id, user_id):
        course = self.course(course_id)
        if not self.can_access(course_id, user_id):
            raise self.error(402, "An active course pass is required. Sign in or review membership options.")
        return course

    @staticmethod
    def stub_stage(stage):
        return {"id": stage["id"], "order": stage.get("order"), "title": stage.get("title"), "titleEn": stage.get("titleEn"),
                "steps": [{"id": s["id"], "order": s.get("order"), "sequence": s.get("sequence"), "title": s.get("title"), "titleEn": s.get("titleEn"),
                           "locked": True, "prerequisiteIds": s.get("prerequisiteIds", []), "knowledge": [],
                           "quiz": {"question": "", "questionEn": "", "options": ["", "", ""], "optionsEn": ["", "", ""], "answer": 0}} for s in stage.get("steps", [])]}

    def visible_course(self, course, entitled):
        if entitled or not self.protected:
            return {**course, "locked": False}
        stages = course.get("stages", [])
        return {**course, "stages": stages[:FREE_STAGES] + [self.stub_stage(st) for st in stages[FREE_STAGES:]], "locked": False, "paid": True, "partial": True}

    def free_step(self, course, step_id):
        return step_id in {s["id"] for st in course.get("stages", [])[:FREE_STAGES] for s in st.get("steps", [])}

    def curriculum(self, user_id, course_id=None, index=False):
        entitled = not self.protected or bool(self.entitlement(user_id))
        courses=self.load_courses()
        if course_id is not None:
            return self.visible_course(self.course(course_id), entitled)
        result=[self.visible_course(course, entitled) for course in courses.values()]
        if not index:return result
        keys=('id','title','titleEn','category','subcategory','subcategoryTitle','subcategoryTitleEn','summary','summaryEn','status','kind','stepCount','estimatedMinutes','diagram','flowDiagram','photoId','educationEdition','enrichmentVersion','curriculumVersion','contentStatus','depth','languageCoverage','locked','paid','partial')
        return [{**{k:c[k] for k in keys if k in c},'_lazy':True,'stages':[
            {**{k:stage[k] for k in ('id','title','titleEn','order') if k in stage},'steps':[{'id':step['id']} for step in stage.get('steps',[])]}
            for stage in c.get('stages',[])]} for c in result]

    def static_allowed(self, target):
        """An allowlist applied to the resolved path prevents aliases/traversal."""
        if not self.protected:
            return True
        relative = target.relative_to(self.app.public)
        name = relative.as_posix()
        if name=='data/lazy/index.json':return True
        if name.startswith('data/lazy/resources/') and target.suffix in ('.json','.js'):return True
        if name.startswith('data/lazy/courses/'):
            match=re.fullmatch(r'(.+)-[0-9a-f]{16}\.(?:json|js)',target.name)
            return bool(match and match[1] not in self.load_courses())
        if name.startswith('data/lazy/data/'):
            match=re.fullmatch(r'(.+)-[0-9a-f]{16}\.(?:json|js)',target.name)
            return bool(match and match[1] in ('sources','source-usage','media','release','related-skills','course-places','vendors','learning-map'))
        if len(relative.parts) == 1:
            return (target.suffix in (".css", ".js", ".html", ".svg") and
                    not target.name.startswith("offline-data") and target.name not in ("offline-build.json",))
        if relative.parts[0] in ("assets", "vendor"):
            return target.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".svg", ".css", ".js", ".wasm", ".woff", ".woff2", ".txt")
        return name in {f"data/{item}.json" for item in ("catalog", "photos", "sources", "media", "release", "related-skills", "course-places", "vendors")}

    def checkout(self, user_id, payload):
        if not self.available:
            raise self.error(503, self.reason)
        plan = next((p for p in PLANS if p["id"] == payload.get("planId")), None)
        if not plan or payload.get("termsAccepted") is not True or payload.get("termsVersion") != TERMS_VERSION:
            raise self.error(400, "Select a valid plan and accept the current terms.")
        request_key = payload.get("requestId")
        if not isinstance(request_key, str) or not re.fullmatch(r"[A-Za-z0-9_-]{16,80}", request_key):
            raise self.error(400, "Provide a unique requestId of 16–80 letters, digits, underscores or hyphens.")
        now = int(time.time())
        with self.app.db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM commerce_orders WHERE user_id=? AND request_key=?", (user_id, request_key)).fetchone()
            if row:
                if row["plan_id"] != plan["id"] or row["mode"] != self.mode or row["status"] != "pending" or row["created_at"] < now - 3600:
                    raise self.error(409, "This checkout request has already been used or expired.")
            else:
                if db.execute("SELECT count(*) FROM commerce_orders WHERE user_id=? AND created_at>?", (user_id, now - 3600)).fetchone()[0] >= 10:
                    raise self.error(429, "Too many checkout attempts; try later.")
                order_id = "MG" + secrets.token_hex(9).upper()
                trade_date = datetime.fromtimestamp(now, timezone(timedelta(hours=8))).strftime("%Y/%m/%d %H:%M:%S")
                db.execute("INSERT INTO commerce_orders(id,user_id,plan_id,amount,duration_days,mode,status,created_at,trade_date,terms_version,request_key) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (order_id, user_id, plan["id"], plan["amountTwd"], plan["durationDays"], self.mode, "pending", now, trade_date, TERMS_VERSION, request_key))
                row = db.execute("SELECT * FROM commerce_orders WHERE id=?", (order_id,)).fetchone()
        fields = {"MerchantID": self.merchant, "MerchantTradeNo": row["id"], "MerchantTradeDate": row["trade_date"], "PaymentType": "aio", "TotalAmount": str(row["amount"]), "TradeDesc": "MacGyver Engineering Academy course access", "ItemName": f"MacGyver Academy {row['duration_days']} days", "ReturnURL": self.app.origin + "/api/billing/ecpay/notify", "ClientBackURL": self.app.origin + "/#membership", "ChoosePayment": "Credit", "EncryptType": "1"}
        fields["CheckMacValue"] = check_mac(fields, self.key, self.iv)
        host = "payment-stage.ecpay.com.tw" if self.mode == "sandbox" else "payment.ecpay.com.tw"
        return {"action": f"https://{host}/Cashier/AioCheckOut/V5", "fields": fields, "orderId": row["id"], "mode": self.mode}

    def query_transport(self, url, body):
        request = Request(url, data=body, method="POST", headers={"Content-Type": "application/x-www-form-urlencoded"})
        try:
            with build_opener(NoPaymentRedirect()).open(request, timeout=15) as response:
                raw = response.read(32769)
                if len(raw) > 32768:
                    raise self.error(502, "Provider verification response is too large.")
                return raw
        except (HTTPError, URLError, TimeoutError, OSError):
            raise self.error(503, "Provider order verification is temporarily unavailable. No access was granted; retry notification later.") from None

    def query_order(self, order_id):
        if not self.available or not re.fullmatch(r"MG[A-F0-9]{18}", order_id):
            raise self.error(503, "Order verification is unavailable.")
        fields = {"MerchantID": self.merchant, "MerchantTradeNo": order_id, "TimeStamp": str(int(time.time()))}
        fields["CheckMacValue"] = check_mac(fields, self.key, self.iv)
        host = "payment-stage.ecpay.com.tw" if self.mode == "sandbox" else "payment.ecpay.com.tw"
        raw = self.query_transport(f"https://{host}/Cashier/QueryTradeInfo/V5", urlencode(fields).encode())
        result = parse_notification(raw, self.error)
        signature = result.get("CheckMacValue", "")
        if not re.fullmatch(r"[a-fA-F0-9]{64}", signature) or not hmac.compare_digest(signature.upper(), check_mac(result, self.key, self.iv)):
            raise self.error(502, "Provider order verification signature failed.")
        if result.get("MerchantID") != self.merchant or result.get("MerchantTradeNo") != order_id:
            raise self.error(502, "Provider order verification identity mismatch.")
        return result

    def notification(self, raw, verified_query=None):
        if not self.available:
            raise self.error(503, "Payment notification endpoint is not configured.")
        fields = parse_notification(raw, self.error)
        supplied = fields.get("CheckMacValue", "")
        if not re.fullmatch(r"[A-Fa-f0-9]{64}", supplied) or not hmac.compare_digest(supplied.upper(), check_mac(fields, self.key, self.iv)):
            raise self.error(400, "Invalid payment signature.")
        if fields.get("MerchantID") != self.merchant or not re.fullmatch(r"MG[A-F0-9]{18}", fields.get("MerchantTradeNo", "")):
            raise self.error(400, "Invalid payment merchant or order.")
        amount = fields.get("TradeAmt", "")
        if not re.fullmatch(r"[1-9][0-9]{0,8}", amount):
            raise self.error(400, "Invalid payment amount.")
        digest = hashlib.sha256(json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        now = int(time.time())
        with self.app.db() as db:
            stored = db.execute("SELECT * FROM commerce_orders WHERE id=?", (fields["MerchantTradeNo"],)).fetchone()
            if not stored or stored["mode"] != self.mode or stored["amount"] != int(amount):
                raise self.error(400, "Payment does not match the stored order.")
            if db.execute("SELECT 1 FROM commerce_events WHERE digest=?", (digest,)).fetchone():
                return "1|OK"
        # A signed notification alone is insufficient for first fulfilment:
        # independently query the fixed ECPay endpoint, outside the DB write lock.
        if fields.get("RtnCode") == "1" and fields.get("SimulatePaid") == "0" and stored["status"] == "pending":
            query = verified_query or self.query_order(stored["id"])
            if query.get("TradeStatus") != "1" or any(query.get(k) != fields.get(k) for k in ("MerchantID", "MerchantTradeNo", "TradeAmt", "TradeNo", "PaymentType")):
                raise self.error(503, "Provider has not independently confirmed this payment. No access was granted.")
        with self.app.db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM commerce_orders WHERE id=?", (fields["MerchantTradeNo"],)).fetchone()
            if not row or row["mode"] != self.mode or row["amount"] != int(amount):
                raise self.error(400, "Payment does not match the stored order.")
            if db.execute("SELECT 1 FROM commerce_events WHERE digest=?", (digest,)).fetchone():
                return "1|OK"
            success = fields.get("RtnCode") == "1"
            simulated = fields.get("SimulatePaid") != "0"
            # Even in sandbox SimulatePaid=1 is only a connectivity probe and
            # never grants access. A staged checkout with SimulatePaid=0 grants
            # a sandbox-only entitlement, which live mode cannot read.
            result = "simulated-ignored" if simulated else "paid" if success else "not-paid"
            if success and not simulated:
                trade = fields.get("TradeNo", "")
                if not re.fullmatch(r"[A-Za-z0-9]{1,20}", trade) or not fields.get("PaymentType", "").startswith("Credit"):
                    raise self.error(400, "Invalid payment trade or payment method.")
                duplicate = db.execute("SELECT id FROM commerce_orders WHERE provider_trade=? AND id<>?", (trade, row["id"])).fetchone()
                if duplicate or (row["provider_trade"] and row["provider_trade"] != trade):
                    raise self.error(409, "Payment trade conflicts with a stored order.")
                if row["status"] not in ("revoked", "refunded"):
                    if row["status"] != "paid":
                        future = db.execute("SELECT max(expires_at) FROM commerce_entitlements WHERE user_id=? AND mode=? AND revoked_at IS NULL", (row["user_id"], self.mode)).fetchone()[0] or now
                        starts = max(now, future)
                        db.execute("INSERT INTO commerce_entitlements VALUES(?,?,?,?,?,NULL)", (row["id"], row["user_id"], self.mode, starts, starts + row["duration_days"] * 86400))
                        db.execute("UPDATE commerce_orders SET status='paid',provider_trade=?,paid_at=?,last_code='1' WHERE id=?", (trade, now, row["id"]))
                else:
                    result = "revoked-no-grant"
            elif not simulated and row["status"] == "pending":
                db.execute("UPDATE commerce_orders SET last_code=? WHERE id=?", (fields.get("RtnCode", "")[:30], row["id"]))
            db.execute("INSERT INTO commerce_events VALUES(?,?,?,?)", (digest, row["id"], now, result))
        return "1|OK"

    def reconcile(self, order_id):
        """Administrator-only recovery of missed notifications via signed query."""
        with self.app.db() as db:
            row = db.execute("SELECT * FROM commerce_orders WHERE id=?", (order_id,)).fetchone()
        if not row or row["mode"] != self.mode:
            raise self.error(404, "Order not found in this payment environment.")
        query = self.query_order(order_id)
        if query.get("TradeStatus") != "1":
            return {"orderId": order_id, "providerStatus": query.get("TradeStatus"), "granted": False}
        fields = {k: query[k] for k in ("MerchantID", "MerchantTradeNo", "TradeAmt", "TradeNo", "PaymentType") if k in query}
        fields.update({"RtnCode": "1", "SimulatePaid": "0", "PaymentDate": query.get("PaymentDate", "")})
        fields["CheckMacValue"] = check_mac(fields, self.key, self.iv)
        self.notification(urlencode(fields).encode(), verified_query=query)
        with self.app.db() as db:
            status = db.execute("SELECT status FROM commerce_orders WHERE id=?", (order_id,)).fetchone()[0]
        return {"orderId": order_id, "providerStatus": "1", "status": status, "granted": status == "paid"}

    def account(self, user_id):
        with self.app.db() as db:
            entitlements = [dict(r) for r in db.execute("SELECT order_id AS orderId,mode,starts_at AS startsAt,expires_at AS expiresAt,revoked_at AS revokedAt FROM commerce_entitlements WHERE user_id=? ORDER BY expires_at DESC LIMIT 100", (user_id,))]
            orders = [dict(r) for r in db.execute("SELECT id,plan_id AS planId,amount AS amountTwd,mode,status,created_at AS createdAt,paid_at AS paidAt FROM commerce_orders WHERE user_id=? ORDER BY created_at DESC LIMIT 100", (user_id,))]
        return {"entitlements": entitlements, "orders": orders, "active": bool(self.entitlement(user_id))}

    def evidence(self, user_id, payload):
        if not self.protected:
            raise self.error(409, "The demo edition creates local learning statements, not server certificates.")
        course = self.course(payload.get("courseId"))
        if not self.can_access(course["id"], user_id) and not self.free_step(course, payload.get("stepId")):
            raise self.error(402, "This step is beyond the free first section. Activate a learning pass.")
        rev, sequence = self.course_revision(course), steps(course)
        if payload.get("revision") != rev:
            raise self.error(409, "Course revision changed; reload the course evidence status.")
        step_id, answer = payload.get("stepId"), payload.get("answer")
        if not isinstance(answer, int) or isinstance(answer, bool):
            raise self.error(400, "Provide a numeric quiz answer.")
        position = next((i for i, s in enumerate(sequence) if s["id"] == step_id), -1)
        if position < 0:
            raise self.error(400, "Unknown step.")
        now = int(time.time())
        mode = self.evidence_mode(course["id"], course, step_id)
        modes = self.evidence_modes()
        with self.app.db() as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("INSERT INTO evidence_attempts VALUES(?,?,1) ON CONFLICT(user_id,hour) DO UPDATE SET count=count+1", (user_id, now // 3600))
            attempts = db.execute("SELECT count FROM evidence_attempts WHERE user_id=? AND hour=?", (user_id, now // 3600)).fetchone()[0]
            db.execute("DELETE FROM evidence_attempts WHERE user_id=? AND hour<?", (user_id, now // 3600 - 48))
            if attempts > 240:
                # Commit the limit counter; do not roll it back by raising here.
                limited = True
            else:
                limited = False
                passed = {r[0] for r in db.execute(f"SELECT step_id FROM learning_evidence WHERE user_id=? AND course_id=? AND revision=? AND mode IN ({','.join('?' * len(modes))})", (user_id, course["id"], rev, *modes))}
                if any(s["id"] not in passed for s in sequence[:position]):
                    raise self.error(409, "Complete the preceding server-recorded quiz steps first.")
                if answer != sequence[position].get("quiz", {}).get("answer"):
                    return {"passed": False, "stepId": step_id, "completed": len(passed), "total": len(sequence)}
                db.execute("INSERT OR IGNORE INTO learning_evidence VALUES(?,?,?,?,?,?)", (user_id, course["id"], rev, step_id, now, mode))
                count = len(passed | {step_id})
        if limited:
            raise self.error(429, "Quiz attempt limit reached; try next hour.")
        return {"passed": True, "stepId": step_id, "completed": count, "total": len(sequence)}

    def evidence_status(self, user_id, course_id):
        course = self.course(course_id)
        rev = self.course_revision(course)
        modes = self.evidence_modes()
        with self.app.db() as db:
            passed = list(dict.fromkeys(r[0] for r in db.execute(f"SELECT step_id FROM learning_evidence WHERE user_id=? AND course_id=? AND revision=? AND mode IN ({','.join('?' * len(modes))}) ORDER BY passed_at,step_id", (user_id, course_id, rev, *modes))))
        return {"courseId": course_id, "revision": rev, "completed": passed, "total": len(steps(course)), "mode": modes[-1]}

    def evidence_mode(self, course_id, course=None, step_id=None):
        # V12: evidence for the free first stage survives when the operator later
        # enables live checkout. Sandbox evidence is always isolated.
        if self.mode == "sandbox":
            return "sandbox"
        if course_id in FREE_COURSES or (course is not None and step_id and self.free_step(course, step_id)):
            return "free"
        return self.mode

    def evidence_modes(self):
        return ("sandbox",) if self.mode == "sandbox" else ("free", self.mode)

    def issue_certificate(self, user, payload):
        if not self.protected:
            raise self.error(409, "Certificates require a protected learning server.")
        course = self.require_access(payload.get("courseId"), user["id"])
        rev, sequence = self.course_revision(course), steps(course)
        mode = "sandbox" if self.mode == "sandbox" else self.mode
        modes = self.evidence_modes()
        with self.app.db() as db:
            db.execute("BEGIN IMMEDIATE")
            evidence = {r[0] for r in db.execute(f"SELECT step_id FROM learning_evidence WHERE user_id=? AND course_id=? AND revision=? AND mode IN ({','.join('?' * len(modes))})", (user["id"], course["id"], rev, *modes))}
            if not sequence or any(s["id"] not in evidence for s in sequence):
                raise self.error(409, "All course quiz steps must first pass on this server.")
            old = db.execute("SELECT * FROM learning_certificates WHERE user_id=? AND course_id=? AND revision=? AND mode=?", (user["id"], course["id"], rev, mode)).fetchone()
            if old:
                if old["revoked_at"]:
                    raise self.error(409, "This certificate was revoked. Contact the course administrator.")
                certificate_id = old["id"]
            else:
                entitlement = self.entitlement(user["id"], db) if course["id"] not in FREE_COURSES else None
                if course["id"] not in FREE_COURSES and not entitlement:
                    raise self.error(402, "An active course pass is required.")
                certificate_id = secrets.token_hex(20)
                public_name = user["name"] if payload.get("publishName") is True else "Learner"
                db.execute("INSERT INTO learning_certificates VALUES(?,?,?,?,?,?,?,?,?,?,?,NULL)", (certificate_id, user["id"], course["id"], rev, course["title"], course.get("titleEn", course["title"]), len(sequence), public_name, int(time.time()), mode, entitlement["order_id"] if entitlement else None))
        return self.verify_certificate(certificate_id)

    def verify_certificate(self, certificate_id):
        if not re.fullmatch(r"[a-f0-9]{40}", certificate_id):
            raise self.error(404, "Certificate not found.")
        with self.app.db() as db:
            row = db.execute("SELECT * FROM learning_certificates WHERE id=?", (certificate_id,)).fetchone()
        if not row:
            raise self.error(404, "Certificate not found.")
        # No account ID, email, order number or payment information is public.
        return {"id": row["id"], "valid": row["revoked_at"] is None, "revoked": row["revoked_at"] is not None,
                "courseId": row["course_id"], "courseTitle": row["course_title"], "courseTitleEn": row["course_title_en"],
                "revision": row["revision"], "steps": row["step_count"], "displayName": row["public_name"],
                "issuedAt": row["issued_at"], "mode": row["mode"], "sandbox": row["mode"] == "sandbox",
                "verificationUrl": self.app.origin + "/api/certificates/" + row["id"],
                "claim": "Completion of this platform's server-recorded course quizzes. Not a degree, professional licence, proctored examination or verification of physical assembly skills."}

    def revoke_order(self, order_id, reason):
        """Local administrator command only; does NOT move money or issue refunds."""
        if not re.fullmatch(r"MG[A-F0-9]{18}", order_id) or not isinstance(reason, str) or not 4 <= len(reason.strip()) <= 500:
            raise self.error(400, "A valid order and an audit reason are required.")
        now = int(time.time())
        with self.app.db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT id FROM commerce_orders WHERE id=?", (order_id,)).fetchone()
            if not row:
                raise self.error(404, "Order not found.")
            db.execute("UPDATE commerce_orders SET status='revoked' WHERE id=?", (order_id,))
            db.execute("UPDATE commerce_entitlements SET revoked_at=COALESCE(revoked_at,?) WHERE order_id=?", (now, order_id))
            db.execute("UPDATE learning_certificates SET revoked_at=COALESCE(revoked_at,?) WHERE order_id=?", (now, order_id))
            db.execute("INSERT INTO commerce_admin_audit(order_id,action,reason,at) VALUES(?,?,?,?)", (order_id, "revoke-access-only", reason.strip(), now))
        return {"orderId": order_id, "revoked": True, "moneyRefunded": False}


def dispatch_commerce(handler, path):
    """Return True when handled; shared same-origin/cookie checks remain in Handler."""
    commerce = handler.app.commerce
    method = handler.command
    if method == "GET" and path == "/api/billing/config":
        handler.send_json(commerce.config())
    elif method == "GET" and path == "/api/billing/me":
        handler.send_json(commerce.account(handler.user(True)["id"]))
    elif method == "GET" and path == "/api/curriculum":
        query=parse_qsl(urlsplit(handler.path).query,keep_blank_values=True)
        if len(query)>1 or any(k not in ('courseId','index') for k,v in query):raise commerce.error(400,'Invalid curriculum query.')
        values=dict(query)
        if 'index' in values and values['index']!='1':raise commerce.error(400,'index must be 1.')
        if 'courseId' in values and not re.fullmatch(r'[a-z0-9]+(?:[-_][a-z0-9]+)*',values['courseId']):raise commerce.error(400,'Invalid courseId.')
        handler.send_json(commerce.curriculum((handler.user() or {}).get('id'),course_id=values.get('courseId'),index=values.get('index')=='1'))
    elif method == "GET" and path.startswith("/api/courses/"):
        uid = (handler.user() or {}).get("id")
        handler.send_json(commerce.visible_course(commerce.course(path.removeprefix("/api/courses/")), commerce.can_access(path.removeprefix("/api/courses/"), uid)))
    elif method == "GET" and path.startswith("/api/learning/"):
        handler.send_json(commerce.evidence_status(handler.user(True)["id"], path.removeprefix("/api/learning/")))
    elif method == "GET" and path == "/api/certificates":
        user = handler.user(True)
        with handler.app.db() as db:
            ids = [r[0] for r in db.execute("SELECT id FROM learning_certificates WHERE user_id=? ORDER BY issued_at DESC LIMIT 2000", (user["id"],))]
        handler.send_json({"certificates": [commerce.verify_certificate(identifier) for identifier in ids]})
    elif method == "GET" and path.startswith("/api/certificates/"):
        certificate = commerce.verify_certificate(path.removeprefix("/api/certificates/"))
        if "text/html" in handler.headers.get("Accept", ""):
            document = certificate_html(certificate).encode("utf-8")
            handler.send_response(200)
            handler.common_headers()
            handler.send_header("Content-Type", "text/html; charset=utf-8")
            handler.send_header("Content-Length", str(len(document)))
            handler.send_header("Cache-Control", "private, no-store")
            handler.end_headers()
            handler.wfile.write(document)
        else:
            handler.send_json(certificate)
    elif method == "POST" and path == "/api/billing/ecpay/notify":
        if handler.headers.get("Transfer-Encoding") or not handler.headers.get("Content-Type", "").lower().startswith("application/x-www-form-urlencoded"):
            raise commerce.error(415, "Use a bounded form-encoded notification.")
        try:
            size = int(handler.headers.get("Content-Length", "0"))
        except ValueError:
            size = 0
        if not 0 < size <= 32768:
            raise commerce.error(413, "Payment notification is missing or too large.")
        raw = handler.rfile.read(size)
        if len(raw) != size:
            raise commerce.error(400, "Incomplete payment notification.")
        result = commerce.notification(raw).encode("ascii")
        handler.send_response(200)
        handler.common_headers()
        handler.send_header("Content-Type", "text/plain; charset=utf-8")
        handler.send_header("Content-Length", str(len(result)))
        handler.send_header("Cache-Control", "no-store")
        handler.end_headers()
        handler.wfile.write(result)
    elif method == "POST" and path in ("/api/billing/checkout", "/api/learning/evidence", "/api/certificates"):
        user = handler.user(True)
        payload = handler.request_body(8192)
        if "expectedUserId" in payload and payload["expectedUserId"] != user["id"]:
            raise commerce.error(409, "The learning account changed. Reload and retry with the current account.")
        if path == "/api/billing/checkout":
            result = commerce.checkout(user["id"], payload)
        elif path == "/api/learning/evidence":
            result = commerce.evidence(user["id"], payload)
        else:
            result = commerce.issue_certificate(user, payload)
        handler.send_json(result)
    else:
        return False
    return True


def certificate_html(certificate):
    """Printable HTML is rendered only from an existing server certificate row."""
    safe = {k: html.escape(str(v), quote=True) for k, v in certificate.items()}
    issued = datetime.fromtimestamp(certificate["issuedAt"], timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    label = "已撤銷 · REVOKED" if certificate["revoked"] else "沙盒測試 · SANDBOX TEST" if certificate["sandbox"] else "平台測驗完成紀錄 · PLATFORM COMPLETION RECORD"
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Course completion · {safe['courseTitleEn']}</title><style>
*{{box-sizing:border-box}}body{{margin:0;padding:30px;background:#eaf0f2;color:#203440;font:16px/1.65 system-ui,sans-serif}}.tools{{max-width:1050px;margin:0 auto 20px;display:flex;gap:20px;align-items:center}}button{{padding:12px 24px;border:0;border-radius:8px;background:#126574;color:white;font:inherit;cursor:pointer}}article{{max-width:1050px;margin:auto;border:2px solid #7b9aa5;background:#fff;padding:50px;position:relative}}.brand{{font-weight:700;letter-spacing:.12em;color:#126574}}.label{{margin:24px 0;color:{'#a62626' if certificate['revoked'] else '#8a5a12' if certificate['sandbox'] else '#526c78'};font-weight:700}}h1{{font-size:34px;line-height:1.25;margin:10px 0}}h2{{font-size:26px;line-height:1.4}}.en{{color:#526c78}}.name{{font-size:28px;border-bottom:1px solid #b7c8ce;padding-bottom:16px}}.details{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:30px}}.verify{{font:12px/1.8 monospace;overflow-wrap:anywhere;border-top:1px solid #b7c8ce;padding-top:18px;margin-top:30px}}.claim{{font-size:13px;color:#526c78}}a{{color:#126574}}@media(max-width:600px){{body{{padding:12px}}article{{padding:24px}}h1{{font-size:27px}}.details{{grid-template-columns:1fr}}}}@media print{{@page{{size:A4 landscape;margin:12mm}}body{{padding:0;background:white;font-size:12px}}article{{max-width:none;padding:25px;border-width:1px}}.tools{{display:none}}.name{{font-size:23px}}h1{{font-size:28px}}h2{{font-size:22px}}a{{color:inherit;text-decoration:none}}}}
</style></head><body><div class="tools"><button id="print">列印／儲存 PDF · Print / Save PDF</button><a href="/#membership">返回會員 / Membership</a></div><article><div class="brand">MACGYVER ENGINEERING ACADEMY</div><div class="label">{html.escape(label)}</div><h1>課程完成證書<br><span class="en">Certificate of Course Completion</span></h1><p class="name">{safe['displayName']}</p><p>已完成本平台逐步課程之伺服器記錄測驗。<br><span class="en">Completed the server-recorded quizzes for this platform course.</span></p><h2>{safe['courseTitle']}<br><span class="en">{safe['courseTitleEn']}</span></h2><div class="details"><div>完成步驟 / Steps: <strong>{safe['steps']}</strong></div><div>核發時間 / Issued: <strong>{issued}</strong></div></div><p class="claim">此證書不是學位、工程師資格、監考認證或實體工藝技能鑑定。沙盒證書僅供測試。驗證頁可顯示後續撤銷狀態。<br>{safe['claim']}</p><div class="verify">ID: {safe['id']}<br>Course SHA-256: {safe['revision']}<br>線上驗證 / Verify: <a href="{safe['verificationUrl']}">{safe['verificationUrl']}</a></div></article><script>document.getElementById('print').addEventListener('click',()=>window.print());</script></body></html>'''
