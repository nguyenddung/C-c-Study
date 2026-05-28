"""File handling utilities: image validation, secure filename generation."""
import imghdr
import uuid
from pathlib import Path

from fastapi import HTTPException, status

from app.core.config import settings


def validate_image_content(content: bytes, allowed_mime_prefixes: list[str] | None = None) -> str:
    """
    Validate that the given bytes represent a valid image.

    Args:
        content: Raw file bytes.
        allowed_mime_prefixes: List of allowed MIME types (e.g. ['image/jpeg', 'image/png']).

    Returns:
        The detected file extension (without dot).

    Raises:
        HTTPException 415 if the content is not a valid image.
    """
    if allowed_mime_prefixes is None:
        allowed_mime_prefixes = settings.allowed_image_types_list

    ext = imghdr.what(None, h=content)
    if ext is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail={"code": "INVALID_IMAGE", "message": "Uploaded file is not a valid image"},
        )

    mime_map = {"jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp", "gif": "image/gif"}
    mime = mime_map.get(ext)
    if not mime or mime not in allowed_mime_prefixes:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail={"code": "UNSUPPORTED_FORMAT", "message": f"Only {', '.join(allowed_mime_prefixes)} allowed"},
        )
    return ext


def generate_secure_filename(user_id: uuid.UUID, extension: str) -> str:
    """Generate a unique filename: {user_id}_{uuid4_short}.{ext}."""
    return f"{user_id}_{uuid.uuid4().hex[:8]}.{extension.lower()}"


def ensure_upload_dirs() -> None:
    """Create upload/avatar and upload/documents directories if missing."""
    Path(settings.UPLOAD_DIR, "avatars").mkdir(parents=True, exist_ok=True)
    Path(settings.UPLOAD_DIR, "documents").mkdir(parents=True, exist_ok=True)