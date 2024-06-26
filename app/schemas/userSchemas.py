from pydantic.types import conint
from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = "member"
    is_active: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class EmailRequest(BaseModel):
    email: EmailStr


class UserGet(UserBase):
    id: int
    created_at: Optional[datetime] = None
    modified: Optional[datetime] = None

    class Config:
        from_attributes = True

class VerifyUserRequest(BaseModel):
    token: str
    email: EmailStr

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    email: str