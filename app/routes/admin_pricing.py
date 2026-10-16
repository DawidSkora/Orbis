from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.database import supabase
from app.deps.auth import require_admin
from app.models.pricing import PricingUpdate
from app.pricing_shared import PRICING_ID, load_pricing_row, row_to_response

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("/")
def get_pricing():
    row = load_pricing_row()
    if not row:
        raise HTTPException(status_code=404, detail="Pricing not configured")
    return row_to_response(row)


@router.put("/")
def update_pricing(body: PricingUpdate):
    document = body.data.to_document()
    now = datetime.now(timezone.utc).isoformat()
    current = load_pricing_row()

    if current is None:
        result = supabase.table("pricing").insert({"id": PRICING_ID, "data": document, "updated_at": now}).execute()
        return row_to_response(result.data[0])

    if body.expected_updated_at and body.expected_updated_at != current["updated_at"]:
        raise HTTPException(status_code=409, detail="Cennik został w międzyczasie zmieniony — odśwież i spróbuj ponownie")

    supabase.table("pricing_revisions").insert({"data": current["data"], "valid_until": now}).execute()
    # Conditional update: only if nobody saved between our read and this write.
    result = (
        supabase.table("pricing")
        .update({"data": document, "updated_at": now})
        .eq("id", PRICING_ID)
        .eq("updated_at", current["updated_at"])
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=409, detail="Cennik został w międzyczasie zmieniony — odśwież i spróbuj ponownie")
    return row_to_response(result.data[0])
