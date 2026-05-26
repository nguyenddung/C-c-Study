"""Notification creation helpers."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification


async def create_notification(
    db: AsyncSession,
    *,
    user_id: UUID,
    type: str,
    title: str,
    body: str | None = None,
    data: dict | None = None,
) -> Notification:
    """Persist a new notification row."""
    notif = Notification(
        user_id=user_id,
        type=type,
        title=title,
        body=body,
        data=data,
    )
    db.add(notif)
    return notif