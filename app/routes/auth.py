import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.database import supabase
from app.deps.auth import create_access_token, require_admin

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    username: str


class MeResponse(BaseModel):
    id: str
    username: str


def _verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest):
    result = (
        supabase.table("admin_users")
        .select("id, username, password_hash, is_active")
        .eq("username", body.username)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = result.data[0]
    if not user.get("is_active"):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not _verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user["id"], user["username"])
    return LoginResponse(token=token, username=user["username"])


@router.get("/me", response_model=MeResponse)
def me(admin: dict = Depends(require_admin)):
    return MeResponse(id=admin["sub"], username=admin.get("username", ""))
