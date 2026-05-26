"""Subject and UserSubject ORM models."""

import uuid

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[str | None] = mapped_column(String(50))  # STEM | Business | Language
    code: Mapped[str | None] = mapped_column(String(20), unique=True)

    user_subjects: Mapped[list["UserSubject"]] = relationship(
        "UserSubject", back_populates="subject"
    )


class UserSubject(Base):
    """Association between a User and a Subject, with skill level."""

    __tablename__ = "user_subjects"
    __table_args__ = (UniqueConstraint("user_id", "subject_id"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        primary_key=True,
    )
    # beginner | intermediate | advanced | expert
    skill_level: Mapped[str] = mapped_column(String(20), default="intermediate")
    # True = wants help, False = can teach
    is_seeking: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship("User", back_populates="user_subjects")  # noqa: F821
    subject: Mapped[Subject] = relationship("Subject", back_populates="user_subjects")