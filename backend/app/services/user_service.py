"""
User service — business logic for user retrieval, search, and update.

Keeps route handlers thin; all DB interaction lives here.
"""

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserUpdateRequest


async def get_user_by_id(user_id: UUID, db: AsyncSession) -> User:
    """Return a User by primary key, or raise 404."""
    result = await db.execute(select(User).where(User.id == user_id, User.is_active == True))  # noqa: E712
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "USER_NOT_FOUND", "message": f"User {user_id} not found"},
        )
    return user


async def search_users(
    db: AsyncSession,
    *,
    q: str | None = None,
    major: str | None = None,
    university: str | None = None,
    limit: int = 20,
    exclude_id: UUID | None = None,
) -> list[User]:
    """
    Full-text search across users using ilike filters.

    Args:
        q:           Partial match on full_name.
        major:       Partial match on major field.
        university:  Partial match on university field.
        limit:       Max results (capped at 50 in router).
        exclude_id:  Exclude this user (usually the current user).

    Returns:
        List of matching active User rows.
    """
    stmt = select(User).where(User.is_active == True)  # noqa: E712

    if exclude_id:
        stmt = stmt.where(User.id != exclude_id)
    if q:
        stmt = stmt.where(User.full_name.ilike(f"%{q}%"))
    if major:
        stmt = stmt.where(User.major.ilike(f"%{major}%"))
    if university:
        stmt = stmt.where(User.university.ilike(f"%{university}%"))

    stmt = stmt.order_by(User.created_at.desc()).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def update_user(user: User, data: UserUpdateRequest, db: AsyncSession) -> User:
    """
    Apply a partial update to *user* from *data*.

    Only fields present (non-None) in *data* are written.
    Validates GPA range (0.0–4.0) and year_of_study (1–6).
    """
    if data.gpa is not None and not (0.0 <= data.gpa <= 4.0):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "INVALID_GPA", "message": "GPA must be between 0.0 and 4.0"},
        )
    if data.year_of_study is not None and not (1 <= data.year_of_study <= 6):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "INVALID_YEAR", "message": "Year of study must be between 1 and 6"},
        )

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(user, field, value)

    # Session tracks the mutation; commit happens in get_db dependency
    return user


async def deactivate_user(user: User, db: AsyncSession) -> None:
    """Soft-delete a user (sets is_active=False)."""
    user.is_active = False