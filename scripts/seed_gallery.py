"""
Seed gallery_photos table and upload images to Supabase Storage.

Prerequisites:
  1. Run supabase/migrations/001_gallery_photos.sql in Supabase SQL Editor
  2. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_ANON_KEY) in .env

Usage (from orbis repo root):
  python scripts/seed_gallery.py
  python scripts/seed_gallery.py --images-dir ../wyczesanalapka/public/images
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

load_dotenv(ROOT / ".env")

from supabase import create_client  # noqa: E402

BUCKET = "gallery"

SEED_ROWS = [
    {
        "pet_name": "Eliot",
        "breed": "Cavalier King Spaniel",
        "service": "Pakiet Pielęgnacyjny",
        "category": "Strzyżenie",
        "aspect_ratio": "portrait",
        "gradient_from": "#FCE4F0",
        "gradient_to": "#F4A7C1",
        "storage_path": "dog-1.webp",
        "sort_order": 1,
        "is_featured": True,
    },
    {
        "pet_name": "Coffe",
        "breed": "Border Collie",
        "service": "Trimowanie i stylizacja",
        "category": "Strzyżenie",
        "aspect_ratio": "square",
        "gradient_from": "#F8F0F5",
        "gradient_to": "#D8B4CC",
        "storage_path": "dog-2.webp",
        "sort_order": 2,
        "is_featured": True,
    },
    {
        "pet_name": "Milo",
        "breed": "Cavalier King Charles Spaniel",
        "service": "Kąpiel i rozczesywanie",
        "category": "Strzyżenie",
        "aspect_ratio": "tall",
        "gradient_from": "#E8D0E0",
        "gradient_to": "#C9A0BC",
        "storage_path": "dog-3.webp",
        "sort_order": 3,
        "is_featured": True,
    },
    {
        "pet_name": "Koka",
        "breed": "Shih Tzu",
        "service": "Strzyżenie higieniczne",
        "category": "Strzyżenie",
        "aspect_ratio": "portrait",
        "gradient_from": "#FCE4F0",
        "gradient_to": "#D8B4CC",
        "storage_path": "dog-4.webp",
        "sort_order": 4,
        "is_featured": True,
    },
    {
        "pet_name": "Maja",
        "breed": "Yorkshire Terrier",
        "service": "Pełen groom z kokardką",
        "category": "Przed & Po",
        "aspect_ratio": "square",
        "gradient_from": "#F8F0F5",
        "gradient_to": "#F4A7C1",
        "storage_path": "dog-5.webp",
        "sort_order": 5,
        "is_featured": True,
    },
    {
        "pet_name": "Borys",
        "breed": "Owczarek Niemiecki",
        "service": "Odświeżenie sierści i wyczesywanie podszerstka",
        "category": "Przed & Po",
        "aspect_ratio": "tall",
        "gradient_from": "#E8D0E0",
        "gradient_to": "#D8B4CC",
        "storage_path": "dog-6.webp",
        "sort_order": 6,
        "is_featured": True,
    },
    {
        "pet_name": "Nala",
        "breed": "Kot Brytyjski Krótkowłosy",
        "service": "Delikatne wyczesywanie i pielęgnacja sierści",
        "category": "Trymowanie",
        "aspect_ratio": "portrait",
        "gradient_from": "#FCE4F0",
        "gradient_to": "#E8D0E0",
        "storage_path": "dog-7.webp",
        "sort_order": 7,
        "is_featured": True,
    },
    {
        "pet_name": "Figa",
        "breed": "Kot Dachowiec",
        "service": "Kąpiel relaksacyjna",
        "category": "Trymowanie",
        "aspect_ratio": "square",
        "gradient_from": "#F8F0F5",
        "gradient_to": "#C9A0BC",
        "storage_path": "dog-8.webp",
        "sort_order": 8,
        "is_featured": True,
    },
    {
        "pet_name": "Kokos",
        "breed": "Królik Mini Lop",
        "service": "Przycinanie pazurków i wyczesywanie",
        "category": "Czesanie",
        "aspect_ratio": "portrait",
        "gradient_from": "#FCE4F0",
        "gradient_to": "#D8B4CC",
        "storage_path": "dog-9.webp",
        "sort_order": 9,
        "is_featured": False,
    },
    {
        "pet_name": "Puszek",
        "breed": "Lagotto",
        "service": "Pielęgnacja długiej sierści",
        "category": "Czesanie",
        "aspect_ratio": "square",
        "gradient_from": "#F8F0F5",
        "gradient_to": "#F4A7C1",
        "storage_path": "dog-10.webp",
        "sort_order": 10,
        "is_featured": False,
    },
    {
        "pet_name": "Rocky",
        "breed": "Labrador Retriever",
        "service": "Kąpiel, suszenie i wyczesywanie",
        "category": "Strzyżenie",
        "aspect_ratio": "square",
        "gradient_from": "#FCE4F0",
        "gradient_to": "#C9A0BC",
        "storage_path": "dog-11.webp",
        "sort_order": 11,
        "is_featured": False,
    },
    {
        "pet_name": "Salon",
        "breed": "Mieszaniec",
        "service": "Metamorfoza: pełen groom",
        "category": "Przed & Po",
        "aspect_ratio": "portrait",
        "gradient_from": "#E8D0E0",
        "gradient_to": "#F4A7C1",
        "storage_path": "dog-12.webp",
        "sort_order": 12,
        "is_featured": False,
    },
]


def _client():
    url = os.environ["SUPABASE_URL"]
    key = (
        os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        or os.environ.get("SUPABASE_ANON_KEY")
        or os.environ.get("SUPABASE_KEY")
    )
    if not key:
        raise SystemExit("Missing Supabase key in .env")
    return create_client(url, key)


def ensure_bucket(supabase) -> None:
    try:
        supabase.storage.create_bucket(BUCKET, options={"public": True})
        print(f"Created bucket '{BUCKET}'")
    except Exception as exc:
        msg = str(exc).lower()
        if "already exists" in msg or "duplicate" in msg:
            print(f"Bucket '{BUCKET}' already exists")
        else:
            print(f"Bucket note: {exc}")


def upload_images(supabase, images_dir: Path) -> None:
    for row in SEED_ROWS:
        filename = row["storage_path"]
        file_path = images_dir / filename
        if not file_path.is_file():
            print(f"Skip missing file: {file_path}")
            continue
        with open(file_path, "rb") as f:
            supabase.storage.from_(BUCKET).upload(
                filename,
                f,
                file_options={"content-type": "image/webp", "upsert": "true"},
            )
        print(f"Uploaded {filename}")


def seed_rows(supabase) -> None:
    existing = supabase.table("gallery_photos").select("id").limit(1).execute()
    if existing.data:
        print("gallery_photos already has rows — skipping insert (delete rows to re-seed)")
        return

    for row in SEED_ROWS:
        row["is_published"] = True

    supabase.table("gallery_photos").insert(SEED_ROWS).execute()
    print(f"Inserted {len(SEED_ROWS)} gallery rows")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--images-dir",
        type=Path,
        default=ROOT.parent / "wyczesanalapka" / "public" / "images",
    )
    parser.add_argument("--skip-upload", action="store_true")
    args = parser.parse_args()

    supabase = _client()
    ensure_bucket(supabase)

    if not args.skip_upload:
        if not args.images_dir.is_dir():
            raise SystemExit(f"Images directory not found: {args.images_dir}")
        upload_images(supabase, args.images_dir)

    seed_rows(supabase)
    print("Done.")


if __name__ == "__main__":
    main()
