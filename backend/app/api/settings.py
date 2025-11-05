from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_db, get_current_admin
from app.models.user import User
from app.models.settings import Settings
from app.schemas.settings import SettingsResponse, SettingsUpdate

router = APIRouter()


@router.get("/admin", response_model=SettingsResponse)
async def get_settings_admin(
    admin: User = Depends(get_current_admin), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Settings).limit(1))
    setting = result.scalars().first()
    if not setting:
        raise HTTPException(status_code=404, detail="Settings not found")
    return setting


@router.post("/admin", response_model=SettingsResponse)
async def update_settings_admin(
    data: SettingsUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Settings).limit(1))
    setting = result.scalars().first()
    if not setting:
        raise HTTPException(status_code=404, detail="Settings not found")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(setting, key, value)

    db.add(setting)
    await db.commit()
    await db.refresh(setting)
    return setting


@router.get("/public", response_model=SettingsResponse, tags=["Public Settings"])
async def get_public_settings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Settings).limit(1))
    setting = result.scalars().first()
    if not setting:
        raise HTTPException(status_code=404, detail="Settings not found")
    return setting
