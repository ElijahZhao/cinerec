"""Authentication endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.database import get_connection

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(req: LoginRequest):
    conn = get_connection()
    user = conn.execute(
        "SELECT id, username FROM users WHERE username = ?", (req.username,)
    ).fetchone()
    conn.close()
    if not user:
        raise HTTPException(404, "User not found / 用户不存在")
    return {"user_id": user["id"], "username": user["username"], "message": "Login success / 登录成功"}


@router.post("/register")
async def register(req: RegisterRequest):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (req.username, req.password)  # Demo: no real hashing
        )
        conn.commit()
        user = conn.execute(
            "SELECT id, username FROM users WHERE username = ?", (req.username,)
        ).fetchone()
        conn.close()
        return {"user_id": user["id"], "username": user["username"], "message": "Registration success / 注册成功"}
    except Exception as e:
        conn.close()
        raise HTTPException(400, f"Username already exists / 用户名已存在")


@router.get("/guest")
async def guest_login():
    """Assign a random existing user for demo."""
    conn = get_connection()
    user = conn.execute("SELECT id, username FROM users ORDER BY RANDOM() LIMIT 1").fetchone()
    conn.close()
    if not user:
        raise HTTPException(404, "No users in database")
    return {"user_id": user["id"], "username": user["username"], "message": "Guest login / 游客登录"}
