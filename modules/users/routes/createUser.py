from fastapi import APIRouter, HTTPException, status
from modules.users.schema.schemas import UserCreate, UserOut
from datetime import datetime
import uuid, hashlib

router = APIRouter()

# in-memory DB
DB = {}

def _hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    for u in DB.values():
        if u["username"] == payload.username:
            raise HTTPException(status_code=400, detail="username exists")
        if u["email"] == payload.email:
            raise HTTPException(status_code=400, detail="email exists")
    uid = str(uuid.uuid4())
    now = datetime.utcnow()
    user = {
        "id": uid,
        "username": payload.username,
        "email": payload.email,
        "role": payload.role,
        "created_at": now,
        "updated_at": now,
        "password": _hash_password(payload.password)
    }
    DB[uid] = user
    return UserOut(**user)
