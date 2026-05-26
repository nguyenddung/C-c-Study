"""Pydantic schemas for the AI matching endpoints."""

from uuid import UUID

from pydantic import BaseModel


class FactorBreakdown(BaseModel):
    subject_score: float
    schedule_score: float
    style_score: float
    goal_score: float
    gpa_score: float


class MatchResult(BaseModel):
    """A single AI-recommended user with scores."""
    user_id: UUID
    full_name: str
    university: str | None
    major: str | None
    gpa: float | None
    avatar_url: str | None
    tags: list[str]  # subject names
    score: float     # 0-100 overall compatibility
    factors: FactorBreakdown
    status: str      # suggested | pending | connected | rejected


class RecommendationsResponse(BaseModel):
    total: int
    results: list[MatchResult]


class ConnectRequest(BaseModel):
    target_user_id: UUID


class MatchStatusResponse(BaseModel):
    match_id: UUID
    status: str