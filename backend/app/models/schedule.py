"""Schedule ORM model — stores a user's available time slots."""

import uuid

from sqlalchemy import ForeignKey, SmallInteger, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Schedule(Base):
    __tablename__ = "schedules"
    __table_args__ = (UniqueConstraint("user_id", "day_of_week", "time_slot"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # 0 = Monday … 6 = Sunday
    day_of_week: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    # e.g. "19-21h"
    time_slot: Mapped[str] = mapped_column(String(10), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="schedules")  # noqa: F821