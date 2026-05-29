import os

GALLERY_BUCKET = "gallery"


def public_image_url(storage_path: str) -> str:
    base = os.environ["SUPABASE_URL"].rstrip("/")
    path = storage_path.lstrip("/")
    return f"{base}/storage/v1/object/public/{GALLERY_BUCKET}/{path}"


def row_to_response(row: dict) -> dict:
    return {
        "id": row["id"],
        "petName": row["pet_name"],
        "breed": row["breed"],
        "service": row["service"],
        "category": row["category"],
        "aspectRatio": row["aspect_ratio"],
        "gradientFrom": row["gradient_from"],
        "gradientTo": row["gradient_to"],
        "imageSrc": public_image_url(row["storage_path"]),
        "storagePath": row["storage_path"],
        "sortOrder": row.get("sort_order", 0),
        "isFeatured": row.get("is_featured", False),
        "isPublished": row.get("is_published", True),
    }
