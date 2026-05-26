from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/whoami")
def whoami(request: Request):
    return {
        "ip": request.client.host,
        "port": request.client.port,
        "user_agent": request.headers.get("user-agent"),
        "method": request.method,
    }
