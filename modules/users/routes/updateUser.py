from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from modules.users.schema.schemas import UserUpdate, UserOut
from modules.users.routes.createUser import DB, _hash_password
from modules.users.routes.readUser import admin_required

router = APIRouter()

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: str, payload: UserUpdate, current=Depends(admin_required)):
    if user_id not in DB:
        raise HTTPException(status_code=404, detail="user not found")

    user = DB[user_id]
    if payload.username:
        if any(u["username"] == payload.username and uid != user_id for uid, u in DB.items()):
            raise HTTPException(status_code=400, detail="username exists")
        user["username"] = payload.username
    if payload.email:
        if any(u["email"] == payload.email and uid != user_id for uid, u in DB.items()):
            raise HTTPException(status_code=400, detail="email exists")
        user["email"] = payload.email
    if payload.role:
        user["role"] = payload.role
    if payload.password:
        user["password"] = _hash_password(payload.password)

    user["updated_at"] = datetime.utcnow()
    DB[user_id] = user
    return UserOut(**user)
