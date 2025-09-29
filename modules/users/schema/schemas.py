from pydantic import BaseModel, EmailStr, validator
from enum import Enum
from typing import Optional
import re
from datetime import datetime

class Role(str, Enum):
    admin = "admin"
    staff = "staff"

USERNAME_REGEX = re.compile(r"^[a-z0-9]{6,15}$")
PASSWORD_REGEX = re.compile(r"^[A-Za-z0-9!@]{8,20}$")

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Role

    @validator("username")
    def username_valid(cls, v):
        if not USERNAME_REGEX.match(v):
            raise ValueError("username must be lowercase alphanumeric, length 6-15")
        return v

class UserCreate(UserBase):
    password: str

    @validator("password")
    def password_valid(cls, v):
        if not PASSWORD_REGEX.match(v):
            raise ValueError("password must be 8-20 chars, only ! and @ allowed")
        if not re.search(r"[A-Z]", v):
            raise ValueError("must contain uppercase")
        if not re.search(r"[a-z]", v):
            raise ValueError("must contain lowercase")
        if not re.search(r"[0-9]", v):
            raise ValueError("must contain digit")
        if not re.search(r"[!@]", v):
            raise ValueError("must contain special char (! or @)")
        return v

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    role: Optional[Role]

class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: Role
    created_at: datetime
    updated_at: datetime
