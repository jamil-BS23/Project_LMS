from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import UserCRUD
from app.dependencies import get_db
from app.core.security import create_access_token, get_current_user
from typing import Optional, List
from app.models.user import User
from app.schemas.auth import CreateUserRequest, CreateUserResponse



router = APIRouter(tags=["Admin"])


@router.post("/createuser", response_model=CreateUserResponse)
async def create_user(
    payload: CreateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user), 
):
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create users",
        )

    existing_user = await UserCRUD.get_user_by_id(db, payload.user_name)
    if existing_user:
        raise HTTPException(status_code=409, detail="USER_NAME_ALREADY_EXISTS")
    
    existing_email = await UserCRUD.get_user_by_email(db, payload.user_email)
    if existing_email:
        raise HTTPException(status_code=409, detail="EMAIL_ALREADY_EXISTS")
    
    user = await UserCRUD.create_user(db, payload)

    return CreateUserResponse(
        user_name=user.user_name,
        user_email=user.user_email,
        role=user.role
    )

