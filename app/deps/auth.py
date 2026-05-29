import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer(auto_error=False)

AUTH_SECRET = os.environ.get("AUTH_SECRET", "")
AUTH_TOKEN_HOURS = int(os.environ.get("AUTH_TOKEN_HOURS", "24"))


def create_access_token(user_id: str, username: str) -> str:
    if not AUTH_SECRET:
        raise RuntimeError("AUTH_SECRET is not set")
    expire = datetime.now(timezone.utc) + timedelta(hours=AUTH_TOKEN_HOURS)
    payload = {
        "sub": user_id,
        "username": username,
        "exp": expire,
    }
    return jwt.encode(payload, AUTH_SECRET, algorithm="HS256")


def decode_token(token: str) -> dict:
    if not AUTH_SECRET:
        raise HTTPException(status_code=500, detail="Auth not configured")
    try:
        return jwt.decode(token, AUTH_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def require_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict:
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return decode_token(credentials.credentials)
