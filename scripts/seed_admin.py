"""
Create an admin user with bcrypt-hashed password.

Prerequisites:
  1. Run supabase/migrations/002_admin_users.sql
  2. SUPABASE_URL and SUPABASE_KEY (service role) in .env

Usage:
  python scripts/seed_admin.py --username admin --password 'your-secure-password'
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import bcrypt
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

load_dotenv(ROOT / ".env")

from app.database import supabase  # noqa: E402


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()

    existing = (
        supabase.table("admin_users")
        .select("id")
        .eq("username", args.username)
        .execute()
    )
    if existing.data:
        print(f"User '{args.username}' already exists — skipping")
        return

    supabase.table("admin_users").insert(
        {
            "username": args.username,
            "password_hash": hash_password(args.password),
            "is_active": True,
        }
    ).execute()
    print(f"Created admin user: {args.username}")


if __name__ == "__main__":
    main()
