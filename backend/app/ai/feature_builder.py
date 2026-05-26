"""
Feature vector builder for the CócStudy recommendation engine.

Each user is represented as a dense float32 vector:

  [subject_vector (50-dim multi-hot)]
  [schedule_vector (42-dim binary: 7 days × 6 time slots)]
  [learning_style (6-dim one-hot)]
  [academic_goal (6-dim one-hot)]
  [gpa_normalized (1-dim)]

  Total: 105 dimensions
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

import numpy as np

# ── Vocabulary lookups ────────────────────────────────────────────────────

# 50 subject slots; subjects not in this list are silently ignored.
SUBJECT_VOCAB: list[str] = [
    "Toán cao cấp", "Vật lý", "Hóa học", "Sinh học", "Lập trình",
    "AI/ML", "Data Science", "Mạng máy tính", "Hệ thống nhúng", "IoT",
    "Marketing", "Kinh tế vi mô", "Kinh tế vĩ mô", "Tài chính", "Kế toán",
    "Quản trị kinh doanh", "Tiếng Anh", "Tiếng Nhật", "Tiếng Hàn", "Dịch thuật",
    "Thiết kế đồ hoạ", "UI/UX", "Kiến trúc", "Nhiếp ảnh", "Videography",
    "Pháp luật", "Luật dân sự", "Luật thương mại", "Y khoa", "Dược học",
    "Điện tử", "Cơ khí", "Xây dựng", "Môi trường", "Năng lượng tái tạo",
    "Tâm lý học", "Xã hội học", "Giáo dục", "Báo chí", "Truyền thông",
    "Python", "Java", "C++", "JavaScript", "SQL",
    "Excel", "Thống kê", "Xác suất", "Vật lý lý thuyết", "Hoá hữu cơ",
]

LEARNING_STYLES: list[str] = [
    "visual", "auditory", "reading", "kinesthetic", "social", "solitary"
]

ACADEMIC_GOALS: list[str] = [
    "exam_prep", "certification", "job_prep", "research", "study_abroad", "startup"
]

# 7 days × 6 time-slot strings (must match Schedule.time_slot values)
DAYS = list(range(7))   # 0=Mon … 6=Sun
TIME_SLOTS: list[str] = ["7-9h", "9-11h", "13-15h", "15-17h", "19-21h", "21-23h"]

FEATURE_DIM = len(SUBJECT_VOCAB) + len(DAYS) * len(TIME_SLOTS) + len(LEARNING_STYLES) + len(ACADEMIC_GOALS) + 1


# ── Data transfer object ──────────────────────────────────────────────────

@dataclass
class UserFeatureInput:
    """Flat representation of a user's matchable attributes."""
    user_id: UUID
    subjects: list[str] = field(default_factory=list)       # subject names
    schedule: list[tuple[int, str]] = field(default_factory=list)  # (day, slot)
    learning_style: str | None = None
    academic_goal: str | None = None
    gpa: float | None = None                                 # 0.0 – 4.0


# ── Builder ───────────────────────────────────────────────────────────────

def build_feature_vector(user: UserFeatureInput) -> np.ndarray:
    """
    Convert a UserFeatureInput into a 105-dim float32 numpy array.

    Args:
        user: Structured input object populated from the database.

    Returns:
        1-D float32 ndarray of shape (FEATURE_DIM,).
    """
    vec = np.zeros(FEATURE_DIM, dtype=np.float32)
    offset = 0

    # 1. Subject multi-hot (50 dims)
    for subj in user.subjects:
        if subj in SUBJECT_VOCAB:
            vec[offset + SUBJECT_VOCAB.index(subj)] = 1.0
    offset += len(SUBJECT_VOCAB)

    # 2. Schedule binary (42 dims: 7 days × 6 slots)
    for day, slot in user.schedule:
        if 0 <= day < 7 and slot in TIME_SLOTS:
            idx = day * len(TIME_SLOTS) + TIME_SLOTS.index(slot)
            vec[offset + idx] = 1.0
    offset += len(DAYS) * len(TIME_SLOTS)

    # 3. Learning style one-hot (6 dims)
    if user.learning_style and user.learning_style in LEARNING_STYLES:
        vec[offset + LEARNING_STYLES.index(user.learning_style)] = 1.0
    offset += len(LEARNING_STYLES)

    # 4. Academic goal one-hot (6 dims)
    if user.academic_goal and user.academic_goal in ACADEMIC_GOALS:
        vec[offset + ACADEMIC_GOALS.index(user.academic_goal)] = 1.0
    offset += len(ACADEMIC_GOALS)

    # 5. GPA normalised to [0, 1] (1 dim)
    if user.gpa is not None:
        vec[offset] = float(user.gpa) / 4.0
    # else leave as 0 (neutral)

    return vec


def build_matrix(users: list[UserFeatureInput]) -> tuple[np.ndarray, list[UUID]]:
    """
    Build a (N × FEATURE_DIM) matrix from a list of users.

    Returns:
        matrix: float32 ndarray of shape (N, FEATURE_DIM)
        ids:    list of UUID in the same row order
    """
    matrix = np.vstack([build_feature_vector(u) for u in users]).astype(np.float32)
    ids = [u.user_id for u in users]
    return matrix, ids