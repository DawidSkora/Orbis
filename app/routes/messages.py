from fastapi import APIRouter, Request
from datetime import datetime
from app.models.message import Message

router = APIRouter()

log = []

@router.post("/log")
def add_log(request: Request, msg: Message):
    entry = {
        "text": msg.text,
        "ip": request.client.host,
        "time": datetime.now().isoformat()
    }
    log.append(entry)
    return entry

@router.get("/log")
def get_log():
    return {"entries": log, "count": len(log)}

@router.post("/message")
def receive_message(msg: Message):
    return {
        "received": msg.text,
        "priority": msg.priority,
        "length": len(msg.text)
    }
