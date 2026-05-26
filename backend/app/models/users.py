"""User ORM model."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Numeric, SmallInteger, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    university: Mapped[str | None] = mapped_column(String(150))
    major: Mapped[str | None] = mapped_column(String(100))
    year_of_study: Mapped[int | None] = mapped_column(SmallInteger)
    gpa: Mapped[float | None] = mapped_column(Numeric(3, 2))
    role: Mapped[str] = mapped_column(String(20), default="student")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    profile: Mapped["Profile"] = relationship(  # noqa: F821
        "Profile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    user_subjects: Mapped[list["UserSubject"]] = relationship(  # noqa: F821
        "UserSubject", back_populates="user", cascade="all, delete-orphan"
    )
    schedules: Mapped[list["Schedule"]] = relationship(  # noqa: F821
        "Schedule", back_populates="user", cascade="all, delete-orphan"
    )