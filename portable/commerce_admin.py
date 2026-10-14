#!/usr/bin/env python3
"""Local administrator commands. No public admin endpoint or refund API."""
import argparse
import json
import os
from pathlib import Path
from .server import ApiError, Application, read_dotenv


def main():
    root = Path(__file__).resolve().parent.parent
    read_dotenv(root / ".env")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=root / "portable/data/macgyver.sqlite3")
    parser.add_argument("--public", type=Path, default=root / "public/academy")
    parser.add_argument("--origin", default=os.environ.get("SITE_ORIGIN", "http://127.0.0.1:8010"))
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status", help="Show capabilities, never credentials")
    orders = commands.add_parser("orders", help="List up to 100 recent orders without account details")
    orders.add_argument("--limit", type=int, default=20)
    reconcile = commands.add_parser("reconcile", help="Query ECPay to recover a missed payment callback")
    reconcile.add_argument("order_id")
    revoke = commands.add_parser("revoke", help="Revoke access and linked certificate only; DOES NOT issue a money refund")
    revoke.add_argument("order_id")
    revoke.add_argument("--reason", required=True)
    args = parser.parse_args()
    if not args.database.is_file():
        parser.error("Database does not exist; start the configured server first.")
    try:
        app = Application(args.database, args.public, args.origin)
        if args.command == "status":
            result = app.commerce.config()
        elif args.command == "orders":
            if not 1 <= args.limit <= 100:
                parser.error("--limit must be 1–100.")
            with app.db() as db:
                result = [dict(row) for row in db.execute("SELECT id,plan_id,amount,mode,status,created_at,paid_at FROM commerce_orders ORDER BY created_at DESC LIMIT ?", (args.limit,))]
        elif args.command == "reconcile":
            result = app.commerce.reconcile(args.order_id)
        else:
            result = app.commerce.revoke_order(args.order_id, args.reason)
    except (ApiError, ValueError) as error:
        parser.exit(1, (error.message if isinstance(error, ApiError) else str(error)) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
