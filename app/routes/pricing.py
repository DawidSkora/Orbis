from fastapi import APIRouter, HTTPException

from app.pricing_shared import load_pricing_row, row_to_response

router = APIRouter()


@router.get("/")
def get_pricing():
    row = load_pricing_row()
    if not row:
        raise HTTPException(status_code=404, detail="Pricing not configured")
    return row_to_response(row)
