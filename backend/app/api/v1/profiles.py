"""Profile routes: get/update own profile and subjects/schedule."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_user, get_db
from app.models.profile import Profile
from app.models.schedule import Schedule
from app.models.subject import UserSubject
from app.models.user import User
from app.schemas.profile import ProfileResponse, ProfileUpdateRequest

router = APIRouter(prefix="/profiles", tags=["profiles"])


async def _get_or_create_profile(user_id: UUID, db: AsyncSession) -> Profile:
    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if profile is None:
        profile = Profile(user_id=user_id)
        db.add(profile)
        await db.flush()
    return profile


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await _get_or_create_profile(current_user.id, db)


@router.put("/me", response_model=ProfileResponse)
async def update_my_profile(
    req: ProfileUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = await _get_or_create_profile(current_user.id, db)

    # Update scalar fields
    for field in ("bio", "learning_style", "academic_goal", "availability", "is_public"):
        val = getattr(req, field)
        if val is not None:
            setattr(profile, field, val)

    # Replace subject associations
    if req.subjects is not None:
        await db.execute(delete(UserSubject).where(UserSubject.user_id == current_user.id))
        for s in req.subjects:
            db.add(UserSubject(
                user_id=current_user.id,
                subject_id=s.subject_id,
                skill_level=s.skill_level,
                is_seeking=s.is_seeking,
            ))

    # Replace schedule slots
    if req.schedule is not None:
        await db.execute(delete(Schedule).where(Schedule.user_id == current_user.id))
        for slot in req.schedule:
            db.add(Schedule(
                user_id=current_user.id,
                day_of_week=slot.day_of_week,
                time_slot=slot.time_slot,
            ))

    return profile


@router.get("/{user_id}", response_model=ProfileResponse)
async def get_public_profile(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Profile).where(Profile.user_id == user_id, Profile.is_public == True)  # noqa: E712
    )
    profile = result.scalar_one_or_none()
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"code": "PROFILE_NOT_FOUND", "message": "Profile not found or private"})
    return profile