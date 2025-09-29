from fastapi import APIRouter, Depends, HTTPException, status
from modules.users.routes.createUser import DB
from modules.users.routes.readUser import admin_required

router = APIRouter()

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, current=Depends(admin_required)):
    if user_id not in DB:
        raise HTTPException(status_code=404, detail="user not found")
    del DB[user_id]
    return None
