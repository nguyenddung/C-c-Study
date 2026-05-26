"""Pydantic schemas for profile endpoints."""

from uuid import UUID

from pydantic import BaseModel


class SubjectIn(BaseModel):
    subject_id: UUID
    skill_level: str = "intermediate"
    is_seeking: bool = True


class ScheduleSlotIn(BaseModel):
    day_of_week: int  # 0=Mon … 6=Sun
    time_slot: str    # e.g. "19-21h"


class ProfileUpdateRequest(BaseModel):
    bio: str | None = None
    learning_style: str | None = None
    academic_goal: str | None = None
    availability: str | None = None
    is_public: bool | None = None
    subjects: list[SubjectIn] | None = None
    schedule: list[ScheduleSlotIn] | None = None


class ProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    avatar_url: str | None = None
    bio: str | None = None
    learning_style: str | None = None
    academic_goal: str | None = None
    availability: str
    xp_points: int
    streak_days: int
    is_public: bool

    model_config = {"from_attributes": True}