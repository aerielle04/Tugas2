"""
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/{user_id}")
def read_user(user_id: int, q: Union[str, None] = None):
    return {"user_id": user_id, "q": q}
"""

#Tugas 2
from fastapi import FastAPI
from modules.users.routes import createUser, readUser, updateUser, deleteUser

app = FastAPI(title="Users CRUD API")

app.include_router(createUser.router)
app.include_router(readUser.router)
app.include_router(updateUser.router)
app.include_router(deleteUser.router)
