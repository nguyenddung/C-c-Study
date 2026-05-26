"""Pydantic schemas for chat/message endpoints."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MessageCreateRequest(BaseModel):
    content: str
    message_type: str = "text"


class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    sender_id: UUID
    content: str
    message_type: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationResponse(BaseModel):
    id: UUID
    other_user_id: UUID
    other_user_name: str
    other_user_avatar: str | None
    last_message: str | None
    unread_count: int
    updated_at: datetime

    model_config = {"from_attributes": True}