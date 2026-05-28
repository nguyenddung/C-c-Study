"""Reusable input validators for Pydantic / FastAPI."""
import re

from fastapi import HTTPException, status


def validate_vietnamese_phone(phone: str) -> str:
    """Validate Vietnamese phone number (10-11 digits, starts with 0)."""
    if not re.match(r"^(0[3|5|7|8|9])+([0-9]{8,9})$", phone):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "INVALID_PHONE", "message": "Số điện thoại không hợp lệ"},
        )
    return phone


def validate_gpa(gpa: float) -> float:
    """Validate GPA is between 0.0 and 4.0."""
    if not (0.0 <= gpa <= 4.0):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "INVALID_GPA", "message": "GPA must be between 0.0 and 4.0"},
        )
    return gpa


def validate_year_of_study(year: int) -> int:
    """Validate year of study (1-6)."""
    if not (1 <= year <= 6):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "INVALID_YEAR", "message": "Year of study must be 1-6"},
        )
    return year