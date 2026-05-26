"""User routes: get/update self, search."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.user import PublicUserResponse, UserResponse, UserUpdateRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_me(
    req: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    for field, value in req.model_dump(exclude_none=True).items():
        setattr(current_user, field, value)
    return current_user


@router.get("/search", response_model=list[PublicUserResponse])
async def search_users(
    q: str | None = Query(None, description="Name search"),
    major: str | None = Query(None),
    university: str | None = Query(None),
    limit: int = Query(20, le=50),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Full-text style search across users (ilike filter)."""
    stmt = select(User).where(User.is_active == True)  # noqa: E712
    if q:
        stmt = stmt.where(User.full_name.ilike(f"%{q}%"))
    if major:
        stmt = stmt.where(User.major.ilike(f"%{major}%"))
    if university:
        stmt = stmt.where(User.university.ilike(f"%{university}%"))
    stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{user_id}", response_model=PublicUserResponse)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"code": "USER_NOT_FOUND", "message": "User not found"})
    return user