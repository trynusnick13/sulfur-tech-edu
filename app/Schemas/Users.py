from pydantic import BaseModel
from typing import Dict


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    repeat_password: str
    first_name: str
    last_name: str


class UserLogin(UserBase):
    password: str


class UserLoginResponse(BaseModel):
    success: bool
    access_token: str
    token_type: str


class UserRegisterResponse(BaseModel):
    success: bool


class UserAvatar(BaseModel):
    image: Dict[str, str]


class FailResponse(BaseModel):
    success: bool
    message: str


class User(UserBase):
    user_id: int
    disabled: bool

    class Config:
        orm_mode = True

