"""File upload routes: avatar images."""

import os
import uuid
from pathlib import Path

import aiofiles
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.dependencies import get_current_user, get_db
from app.models.profile import Profile
from app.models.user import User

router = APIRouter(prefix="/uploads", tags=["uploads"])


class AvatarResponse(BaseModel):
    avatar_url: str


@router.post("/avatar", response_model=AvatarResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a profile avatar image.

    Accepts: JPEG, PNG, WEBP
    Max size: configured via MAX_AVATAR_SIZE_MB
    """
    # Validate content type
    if file.content_type not in settings.allowed_image_types_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_FILE_TYPE", "message": f"Allowed types: {settings.ALLOWED_IMAGE_TYPES}"},
        )

    # Read and validate size
    content = await file.read()
    if len(content) > settings.max_avatar_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={"code": "FILE_TOO_LARGE", "message": f"Max size: {settings.MAX_AVATAR_SIZE_MB}MB"},
        )

    # Determine extension from content type
    ext_map = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}
    ext = ext_map.get(file.content_type, "jpg")

    # Save to disk
    avatar_dir = Path(settings.UPLOAD_DIR) / "avatars"
    avatar_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{current_user.id}_{uuid.uuid4().hex[:8]}.{ext}"
    file_path = avatar_dir / filename

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    avatar_url = f"/static/avatars/{filename}"

    # Update profile
    result = await db.execute(select(Profile).where(Profile.user_id == current_user.id))
    profile = result.scalar_one_or_none()
    if profile:
        profile.avatar_url = avatar_url
    else:
        db.add(Profile(user_id=current_user.id, avatar_url=avatar_url))

    return AvatarResponse(avatar_url=avatar_url)