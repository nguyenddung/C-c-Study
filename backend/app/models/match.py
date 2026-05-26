"""Match ORM model — AI-computed compatibility between two users."""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        # Enforce canonical ordering so (A,B) and (B,A) map to the same row.
        # NOTE: enforced at service layer for async-friendly check.
        CheckConstraint("user_id_a <> user_id_b", name="ck_match_no_self"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id_a: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    user_id_b: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    subject_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    schedule_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    style_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    goal_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    gpa_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    # suggested | pending | connected | rejected
    status: Mapped[str] = mapped_column(String(20), default="suggested")
    initiated_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )