from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.database import supabase
from app.deps.auth import require_admin
from app.models.qa import QAPair, QAPairUpdate

router = APIRouter(dependencies=[Depends(require_admin)])


def _clean(data: dict) -> dict:
    cleaned = {k: v.strip() for k, v in data.items() if v is not None}
    if any(not v for v in cleaned.values()):
        raise HTTPException(status_code=422, detail="Pytanie i odpowiedź nie mogą być puste")
    return cleaned


@router.get("/")
def list_all():
    result = supabase.table("qa_pairs").select("*").order("created_at").execute()
    return result.data


@router.post("/")
def create(pair: QAPair):
    result = supabase.table("qa_pairs").insert(_clean(pair.model_dump())).execute()
    return result.data[0]


@router.put("/{id}")
def update(id: UUID, pair: QAPairUpdate):
    data = _clean(pair.model_dump())
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = supabase.table("qa_pairs").update(data).eq("id", str(id)).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Not found")
    return result.data[0]


@router.delete("/{id}")
def delete(id: UUID):
    result = supabase.table("qa_pairs").delete().eq("id", str(id)).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Not found")
    return {"deleted": str(id)}
