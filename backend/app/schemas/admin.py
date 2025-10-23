
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.models.user import User


class CreateUserRequest(BaseModel):
    user_name: str
    user_email: EmailStr
    password: str
    user_photo: Optional[str] = None
    role: str

class CreateUserResponse(BaseModel):
    user_name: str
    user_email: EmailStr
    role: str
