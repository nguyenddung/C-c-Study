"""Pydantic schemas for study group endpoints."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GroupCreateRequest(BaseModel):
    name: str
    description: str | None = None
    icon: str | None = "📚"
    subject_id: UUID | None = None
    max_members: int = 10
    is_public: bool = True


class GroupMemberResponse(BaseModel):
    user_id: UUID
    full_name: str
    role: str
    joined_at: datetime

    model_config = {"from_attributes": True}


class GroupResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    icon: str | None
    owner_id: UUID
    max_members: int
    next_session: datetime | None
    is_public: bool
    member_count: int
    created_at: datetime

    model_config = {"from_attributes": True}