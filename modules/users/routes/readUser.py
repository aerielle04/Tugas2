from fastapi import APIRouter, Depends, HTTPException, Header, status
from typing import List
from modules.users.schema.schemas import UserOut, Role
from modules.users.routes.createUser import DB

router = APIRouter()

class CurrentUser:
    def __init__(self, user_id: str, role: Role):
        self.id = user_id
        self.role = role

def get_current_user(x_user_id: str = Header(None, alias="X-User-Id"),
                     x_user_role: str = Header(None, alias="X-User-Role")) -> CurrentUser:
    if not x_user_id or not x_user_role:
        raise HTTPException(status_code=403, detail="missing headers")
    if x_user_id not in DB:
        raise HTTPException(status_code=403, detail="user not found")
    if DB[x_user_id]["role"] != x_user_role:
        raise HTTPException(status_code=403, detail="role mismatch")
    return CurrentUser(user_id=x_user_id, role=Role(x_user_role))

def admin_required(current=Depends(get_current_user)):
    if current.role != Role.admin:
        raise HTTPException(status_code=403, detail="admin only")
    return current

@router.get("/users", response_model=List[UserOut])
def read_users(current=Depends(admin_required)):
    return [UserOut(**u) for u in DB.values()]

@router.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: str, current=Depends(get_current_user)):
    if user_id not in DB:
        raise HTTPException(status_code=404, detail="user not found")
    if current.role == Role.admin or current.id == user_id:
        return UserOut(**DB[user_id])
    raise HTTPException(status_code=403, detail="forbidden")
