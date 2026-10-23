#!/usr/bin/env python3
"""Provision the local site owner. No public endpoint grants this role.

The password is read from a terminal (hidden) or stdin, never an argument.
An optional owner-private bootstrap holds only a salted PBKDF2 verifier and
must be kept outside all public source/deployment archives.
"""
import argparse
import base64
import binascii
import getpass
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import sys
import time

from .server import Application, PBKDF2_ROUNDS, read_dotenv

FORMAT = "macgyver-owner-bootstrap-v16"
USERNAME = re.compile(r"[a-z0-9_.-]{3,30}")


def username_value(value):
    if not isinstance(value, str) or not USERNAME.fullmatch(value):
        raise ValueError("Owner username must contain 3–30 lowercase letters, digits, dot, underscore or hyphen.")
    return value


def verifier(username, password):
    username_value(username)
    if not isinstance(password, str) or not 8 <= len(password) <= 256:
        raise ValueError("Owner password must contain 8–256 characters.")
    salt = secrets.token_bytes(32)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ROUNDS)
    return {"format": FORMAT, "username": username, "algorithm": "pbkdf2-sha256",
            "rounds": PBKDF2_ROUNDS, "salt": base64.b64encode(salt).decode("ascii"),
            "passwordHash": base64.b64encode(digest).decode("ascii")}


def validate_verifier(value):
    if not isinstance(value, dict) or set(value) != {"format", "username", "algorithm", "rounds", "salt", "passwordHash"}:
        raise ValueError("Invalid owner bootstrap format.")
    if value["format"] != FORMAT or value["algorithm"] != "pbkdf2-sha256" or type(value["rounds"]) is not int or value["rounds"] != PBKDF2_ROUNDS:
        raise ValueError("Unsupported owner password verifier.")
    username_value(value["username"])
    try:
        salt = base64.b64decode(value["salt"], validate=True)
        digest = base64.b64decode(value["passwordHash"], validate=True)
    except (ValueError, TypeError, binascii.Error):
        raise ValueError("Invalid owner verifier encoding.") from None
    if len(salt) != 32 or len(digest) != 32:
        raise ValueError("Invalid owner verifier size.")
    return value["username"], salt, digest


def write_bootstrap(path, value):
    validate_verifier(value)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation avoids silently replacing an owner's existing secret.
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def provision(app, value, replace_existing=False):
    username, salt, digest = validate_verifier(value)
    with app.db() as db:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute("SELECT id,role FROM users WHERE lower(username)=?", (username,)).fetchone()
        if row and not replace_existing:
            raise ValueError("This username already exists. To explicitly reset its password and grant owner access, add --reset-existing.")
        now = int(time.time())
        if row:
            user_id = row["id"]
            db.execute("UPDATE users SET salt=?,password_hash=?,role='owner' WHERE id=?", (salt, digest, user_id))
            db.execute("DELETE FROM sessions WHERE user_id=?", (user_id,))
            action = "owner-password-reset-and-session-revoke"
        else:
            user_id = secrets.token_hex(16)
            # This local placeholder is never used to send mail. The owner logs
            # in using their username; no invented personal email is required.
            email = user_id + "@owner.invalid"
            db.execute("INSERT INTO users(id,email,name,salt,password_hash,created_at,username,phone,role) VALUES(?,?,?,?,?,?,?,NULL,'owner')",
                       (user_id, email, username, salt, digest, now, username))
            action = "owner-provisioned-locally"
        db.execute("INSERT INTO owner_admin_audit(user_id,action,at) VALUES(?,?,?)", (user_id, action, now))
    return {"username": username, "role": "owner", "allCourses": True, "paymentRequired": False}


def main(argv=None):
    root = Path(__file__).resolve().parent.parent
    read_dotenv(root / ".env")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="kuonanhong")
    parser.add_argument("--database", type=Path, default=root / "portable/data/macgyver.sqlite3")
    parser.add_argument("--public", type=Path, default=root / "public/academy")
    parser.add_argument("--reset-existing", action="store_true", help="Explicitly reset this account; also revoke its sessions")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--password-stdin", action="store_true", help="Read one password line from stdin; never echo it")
    source.add_argument("--bootstrap", type=Path, help="Import an owner-private salted password verifier")
    parser.add_argument("--export-bootstrap", type=Path, help="Write a private verifier file instead of changing the database")
    args = parser.parse_args(argv)
    try:
        if args.bootstrap:
            if args.bootstrap.stat().st_size > 8192:
                raise ValueError("Owner bootstrap exceeds its size limit.")
            value = json.loads(args.bootstrap.read_text(encoding="utf-8"))
            validate_verifier(value)
        else:
            username_value(args.username)
            if args.password_stdin:
                password = sys.stdin.readline(1025).rstrip("\r\n")
            else:
                password = getpass.getpass("管理員密碼 / Owner password: ")
                confirm = getpass.getpass("再次輸入 / Confirm password: ")
                if password != confirm:
                    raise ValueError("The passwords do not match.")
            value = verifier(args.username, password)
            del password
        if args.export_bootstrap:
            path = args.export_bootstrap.expanduser().resolve()
            if path.is_relative_to(args.public.expanduser().resolve()):
                raise ValueError("Owner bootstrap must be outside the public web root.")
            write_bootstrap(path, value)
            print("已建立私有管理員設定（只有加鹽雜湊，沒有明文密碼）。請勿放進公開倉庫。")
            return 0
        app = Application(args.database.expanduser().resolve(), args.public.expanduser().resolve(),
                          os.environ.get("SITE_ORIGIN", "http://127.0.0.1:8010"))
        result = provision(app, value, args.reset_existing)
        print("管理員已設定 / Owner ready: " + result["username"])
        print("全部課程免付費；使用本機／自架伺服器的登入表單登入。")
        print("All lessons are available without payment after signing in to this local/self-hosted server.")
        return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        # The exception messages above never include password/verifier values.
        parser.exit(1, "Owner setup stopped: " + str(error) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
