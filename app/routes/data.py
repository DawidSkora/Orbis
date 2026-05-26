import json
from pathlib import Path
from fastapi import APIRouter, Query
from app.models.message import Message

DATA_FILE = Path("data.json")

router = APIRouter()

@router.get("/stored")
def get_stored():
    if not DATA_FILE.exists():
        return {"items": []}
    return json.loads(DATA_FILE.read_text())

@router.post("/stored")
def save_item(msg: Message):
    data = json.loads(DATA_FILE.read_text()) if DATA_FILE.exists() else {"items": []}
    data["items"].append(msg.text)
    DATA_FILE.write_text(json.dumps(data, indent=2))
    return data


@router.get("/search")
def search(
    keyword: str,
    limit: int = Query(default=10, ge=1, le=100)
):
    fake_db = ["apple", "banana", "apricot", "blueberry"]
    results = [i for i in fake_db if keyword.lower() in i]
    return {"results": results[:limit], "total": len(results)}
