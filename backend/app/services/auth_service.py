"""Authentication business logic."""

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.profile import Profile
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


async def register_user(req: RegisterRequest, db: AsyncSession) -> tuple[User, TokenResponse]:
    """
    Create a new user + empty profile.

    Raises 409 if the email is already registered.
    """
    existing = await db.execute(select(User).where(User.email == req.email))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "EMAIL_EXISTS", "message": "Email already registered"},
        )

    user = User(
        email=req.email,
        password_hash=hash_password(req.password),
        full_name=req.full_name,
        university=req.university,
        major=req.major,
    )
    db.add(user)
    await db.flush()  # get user.id before committing

    # Auto-create an empty profile
    db.add(Profile(user_id=user.id))

    tokens = TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )
    return user, tokens


async def login_user(req: LoginRequest, db: AsyncSession) -> tuple[User, TokenResponse]:
    """Verify credentials and return tokens."""
    result = await db.execute(select(User).where(User.email == req.email))
    user: User | None = result.scalar_one_or_none()

    if user is None or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_CREDENTIALS", "message": "Invalid email or password"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCOUNT_DISABLED", "message": "Account has been disabled"},
        )

    tokens = TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )
    return user, tokens


async def refresh_access_token(refresh_token: str, db: AsyncSession) -> str:
    """Validate a refresh token and issue a new access token."""
    payload = decode_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_REFRESH_TOKEN", "message": "Invalid or expired refresh token"},
        )

    user_id = UUID(payload["sub"])
    result = await db.execute(select(User).where(User.id == user_id, User.is_active == True))  # noqa: E712
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"code": "USER_NOT_FOUND", "message": "User not found"})

    return create_access_token(user.id)