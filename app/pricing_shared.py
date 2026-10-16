from app.database import supabase

PRICING_ID = 1


def load_pricing_row():
    result = supabase.table("pricing").select("*").eq("id", PRICING_ID).execute()
    return result.data[0] if result.data else None


def row_to_response(row: dict) -> dict:
    return {"data": row["data"], "updatedAt": row["updated_at"]}
