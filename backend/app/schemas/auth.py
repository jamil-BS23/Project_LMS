from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    user_id: Optional[str]
    email: Optional[EmailStr]
    password: str


class LoginResponseUser(BaseModel):
    user_id: str
    user_name: str
    user_email: EmailStr
    user_photo: Optional[str]
    role: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: LoginResponseUser
