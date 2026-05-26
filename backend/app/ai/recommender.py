"""
CócStudy AI Recommendation Engine
===================================
Two-stage matching pipeline:

  Stage 1 – KNN retrieval (cosine distance, fast approximate nearest neighbour)
  Stage 2 – Weighted re-scoring using individual factor scores

Architecture is intentionally modular so Stage 1 can be swapped for a
Two-Tower neural network (see app/ai/two_tower/) without changing
the service layer.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

import numpy as np
from sklearn.neighbors import NearestNeighbors

from app.ai.feature_builder import (
    UserFeatureInput,
    build_feature_vector,
    build_matrix,
    SUBJECT_VOCAB,
    TIME_SLOTS,
    LEARNING_STYLES,
    ACADEMIC_GOALS,
)
from app.ai.preprocessor import FeaturePreprocessor

logger = logging.getLogger(__name__)

# ── Weighting config ──────────────────────────────────────────────────────

WEIGHTS: dict[str, float] = {
    "subjects": 0.35,
    "schedule": 0.25,
    "learning_style": 0.15,
    "academic_goal": 0.15,
    "gpa": 0.10,
}

KNN_NEIGHBORS: int = 20
MIN_SCORE: float = 0.0  # include all results; caller may filter


# ── Result dataclass ──────────────────────────────────────────────────────

@dataclass
class MatchScore:
    """Detailed compatibility result for a single candidate."""
    candidate_id: UUID
    total_score: float        # 0 – 100
    subject_score: float
    schedule_score: float
    style_score: float
    goal_score: float
    gpa_score: float


# ── Engine ────────────────────────────────────────────────────────────────

class StudyMatchRecommender:
    """
    Manages the KNN index and computes fine-grained compatibility scores.

    Lifecycle::

        recommender = StudyMatchRecommender()
        recommender.fit(all_users)            # build / rebuild the index
        results = recommender.recommend(query_user, top_k=10)
    """

    def __init__(self, n_neighbors: int = KNN_NEIGHBORS) -> None:
        self._n_neighbors = n_neighbors
        self._preprocessor = FeaturePreprocessor()
        self._knn: NearestNeighbors | None = None
        self._index_ids: list[UUID] = []
        self._raw_inputs: dict[UUID, UserFeatureInput] = {}

    # ── Building the index ────────────────────────────────────────────────

    def fit(self, users: list[UserFeatureInput]) -> None:
        """
        Build the KNN index from *users*.

        Should be called whenever the user-base changes materially
        (e.g., hourly via a background task).

        Args:
            users: All users whose profiles are complete enough to match.
        """
        if len(users) < 2:
            logger.warning("Recommender.fit: fewer than 2 users — index not built.")
            return

        matrix, ids = build_matrix(users)
        X_norm = self._preprocessor.fit_transform(matrix)

        n_neighbors = min(self._n_neighbors, len(users))
        self._knn = NearestNeighbors(
            n_neighbors=n_neighbors,
            metric="cosine",
            algorithm="brute",  # exact; switch to "ball_tree" for > 100k users
        )
        self._knn.fit(X_norm)
        self._index_ids = ids
        self._raw_inputs = {u.user_id: u for u in users}
        logger.info("Recommender index built: %d users", len(users))

    # ── Querying ──────────────────────────────────────────────────────────

    def recommend(
        self,
        query: UserFeatureInput,
        top_k: int = 10,
        exclude_ids: list[UUID] | None = None,
    ) -> list[MatchScore]:
        """
        Return the top-k most compatible users for *query*.

        Args:
            query:      The requesting user's feature input.
            top_k:      Maximum number of results to return.
            exclude_ids: User IDs to exclude (e.g., already-connected users).

        Returns:
            Sorted list of MatchScore (highest score first).
        """
        if self._knn is None:
            logger.warning("recommend() called before fit() — returning empty list.")
            return []

        query_vec = build_feature_vector(query).reshape(1, -1)
        query_norm = self._preprocessor.transform(query_vec)

        distances, indices = self._knn.kneighbors(query_norm)

        exclude_set: set[UUID] = set(exclude_ids or [])
        exclude_set.add(query.user_id)  # never match yourself

        results: list[MatchScore] = []
        for dist, idx in zip(distances[0], indices[0]):
            candidate_id = self._index_ids[idx]
            if candidate_id in exclude_set:
                continue

            candidate = self._raw_inputs.get(candidate_id)
            if candidate is None:
                continue

            score = self._compute_weighted_score(query, candidate)
            results.append(score)

        results.sort(key=lambda r: r.total_score, reverse=True)
        return results[:top_k]

    # ── Pairwise scoring (public — used by /matching/score/{id}) ─────────

    def score_pair(
        self, user_a: UserFeatureInput, user_b: UserFeatureInput
    ) -> MatchScore:
        """Compute detailed compatibility score between two specific users."""
        return self._compute_weighted_score(user_a, user_b)

    # ── Internal helpers ──────────────────────────────────────────────────

    def _compute_weighted_score(
        self, a: UserFeatureInput, b: UserFeatureInput
    ) -> MatchScore:
        """
        Compute a weighted multi-factor compatibility score.

        Each factor returns a value in [0, 1]; final score is scaled to [0, 100].
        """
        s_subj = _subject_overlap(a.subjects, b.subjects)
        s_sched = _schedule_overlap(a.schedule, b.schedule)
        s_style = _exact_match(a.learning_style, b.learning_style)
        s_goal = _exact_match(a.academic_goal, b.academic_goal)
        s_gpa = _gpa_proximity(a.gpa, b.gpa)

        total = (
            WEIGHTS["subjects"] * s_subj
            + WEIGHTS["schedule"] * s_sched
            + WEIGHTS["learning_style"] * s_style
            + WEIGHTS["academic_goal"] * s_goal
            + WEIGHTS["gpa"] * s_gpa
        )

        return MatchScore(
            candidate_id=b.user_id,
            total_score=round(total * 100, 2),
            subject_score=round(s_subj * 100, 2),
            schedule_score=round(s_sched * 100, 2),
            style_score=round(s_style * 100, 2),
            goal_score=round(s_goal * 100, 2),
            gpa_score=round(s_gpa * 100, 2),
        )


# ── Factor scoring functions ──────────────────────────────────────────────

def _subject_overlap(a: list[str], b: list[str]) -> float:
    """Jaccard similarity between two subject lists."""
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 0.5  # neutral when neither has data
    union = sa | sb
    if not union:
        return 0.0
    return len(sa & sb) / len(union)


def _schedule_overlap(
    a: list[tuple[int, str]], b: list[tuple[int, str]]
) -> float:
    """
    Fraction of user-A's available slots that overlap with user-B.

    Returns 0.5 if either user has no schedule (neutral, not penalty).
    """
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.5
    return len(sa & sb) / len(sa)


def _exact_match(a: str | None, b: str | None) -> float:
    """1.0 if both values are equal and non-None, 0.5 if either is None, else 0.0."""
    if a is None or b is None:
        return 0.5
    return 1.0 if a == b else 0.0


def _gpa_proximity(a: float | None, b: float | None) -> float:
    """
    Score based on GPA distance.  Max difference is 4.0; we invert so
    identical GPAs score 1.0 and maximum distance scores 0.0.
    """
    if a is None or b is None:
        return 0.5
    return 1.0 - (abs(a - b) / 4.0)


# ── Module-level singleton (initialised lazily by matching_service) ───────
recommender = StudyMatchRecommender()