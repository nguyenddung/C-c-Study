"""Pydantic schemas for user-related responses."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    university: str | None = None
    major: str | None = None
    year_of_study: int | None = None
    gpa: float | None = None


class UserResponse(UserBase):
    id: UUID
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdateRequest(BaseModel):
    full_name: str | None = None
    university: str | None = None
    major: str | None = None
    year_of_study: int | None = None
    gpa: float | None = None


class PublicUserResponse(BaseModel):
    """Minimal public view of a user (shown to other users)."""
    id: UUID
    full_name: str
    university: str | None = None
    major: str | None = None
    gpa: float | None = None

    model_config = {"from_attributes": True}