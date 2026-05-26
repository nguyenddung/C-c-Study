"""
Matching service — bridges the database and the AI recommender.

Responsibilities:
- Load user feature data from Postgres
- Call recommender.fit() (index rebuild)
- Translate MatchScore → MatchResult schema objects
- Persist computed scores back to the matches table
"""

from __future__ import annotations

import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.ai.feature_builder import UserFeatureInput
from app.ai.recommender import MatchScore, recommender
from app.models.match import Match
from app.models.profile import Profile
from app.models.schedule import Schedule
from app.models.subject import UserSubject
from app.models.user import User
from app.schemas.matching import FactorBreakdown, MatchResult

logger = logging.getLogger(__name__)


async def _load_feature_input(user_id: UUID, db: AsyncSession) -> UserFeatureInput | None:
    """Load a single user's matchable attributes from the DB."""
    # User + profile
    user_result = await db.execute(
        select(User)
        .options(selectinload(User.profile), selectinload(User.user_subjects).selectinload(UserSubject.subject), selectinload(User.schedules))
        .where(User.id == user_id, User.is_active == True)  # noqa: E712
    )
    user: User | None = user_result.scalar_one_or_none()
    if user is None:
        return None

    subjects = [us.subject.name for us in user.user_subjects if us.subject]
    schedule = [(s.day_of_week, s.time_slot) for s in user.schedules]
    profile: Profile | None = user.profile

    return UserFeatureInput(
        user_id=user.id,
        subjects=subjects,
        schedule=schedule,
        learning_style=profile.learning_style if profile else None,
        academic_goal=profile.academic_goal if profile else None,
        gpa=float(user.gpa) if user.gpa is not None else None,
    )


async def rebuild_index(db: AsyncSession) -> int:
    """
    Load all active users and rebuild the KNN index.

    Returns the number of users indexed.
    """
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.profile),
            selectinload(User.user_subjects).selectinload(UserSubject.subject),
            selectinload(User.schedules),
        )
        .where(User.is_active == True)  # noqa: E712
    )
    users = result.scalars().all()

    feature_inputs: list[UserFeatureInput] = []
    for user in users:
        subjects = [us.subject.name for us in user.user_subjects if us.subject]
        schedule = [(s.day_of_week, s.time_slot) for s in user.schedules]
        profile: Profile | None = user.profile
        feature_inputs.append(
            UserFeatureInput(
                user_id=user.id,
                subjects=subjects,
                schedule=schedule,
                learning_style=profile.learning_style if profile else None,
                academic_goal=profile.academic_goal if profile else None,
                gpa=float(user.gpa) if user.gpa is not None else None,
            )
        )

    recommender.fit(feature_inputs)
    logger.info("Index rebuilt for %d users", len(feature_inputs))
    return len(feature_inputs)


async def get_recommendations(
    current_user: User,
    db: AsyncSession,
    limit: int = 20,
    offset: int = 0,
) -> list[MatchResult]:
    """Return AI-recommended study partners for *current_user*."""
    query_input = await _load_feature_input(current_user.id, db)
    if query_input is None:
        return []

    # Load all users for a fresh context if index is empty
    if recommender._knn is None:
        await rebuild_index(db)

    raw_scores: list[MatchScore] = recommender.recommend(
        query_input, top_k=limit + offset
    )
    raw_scores = raw_scores[offset:]

    # Load supplementary display data for the candidates
    candidate_ids = [s.candidate_id for s in raw_scores]
    if not candidate_ids:
        return []

    users_result = await db.execute(
        select(User)
        .options(selectinload(User.profile), selectinload(User.user_subjects).selectinload(UserSubject.subject))
        .where(User.id.in_(candidate_ids))
    )
    users_map: dict[UUID, User] = {u.id: u for u in users_result.scalars().all()}

    # Determine existing match statuses
    match_result = await db.execute(
        select(Match).where(
            (Match.user_id_a == current_user.id) | (Match.user_id_b == current_user.id)
        )
    )
    existing_matches: dict[UUID, str] = {}
    for m in match_result.scalars().all():
        other = m.user_id_b if m.user_id_a == current_user.id else m.user_id_a
        existing_matches[other] = m.status

    results: list[MatchResult] = []
    for score in raw_scores:
        user = users_map.get(score.candidate_id)
        if not user:
            continue
        tags = [us.subject.name for us in user.user_subjects if us.subject]
        avatar = user.profile.avatar_url if user.profile else None

        results.append(
            MatchResult(
                user_id=user.id,
                full_name=user.full_name,
                university=user.university,
                major=user.major,
                gpa=float(user.gpa) if user.gpa else None,
                avatar_url=avatar,
                tags=tags[:5],  # cap display tags
                score=score.total_score,
                factors=FactorBreakdown(
                    subject_score=score.subject_score,
                    schedule_score=score.schedule_score,
                    style_score=score.style_score,
                    goal_score=score.goal_score,
                    gpa_score=score.gpa_score,
                ),
                status=existing_matches.get(user.id, "suggested"),
            )
        )

    return results


async def get_compatibility_score(
    current_user: User, target_user_id: UUID, db: AsyncSession
) -> MatchResult | None:
    """Compute (or retrieve) detailed compatibility between two users."""
    query_input = await _load_feature_input(current_user.id, db)
    target_input = await _load_feature_input(target_user_id, db)
    if query_input is None or target_input is None:
        return None

    score = recommender.score_pair(query_input, target_input)

    # Load display info for target
    target_result = await db.execute(
        select(User)
        .options(selectinload(User.profile), selectinload(User.user_subjects).selectinload(UserSubject.subject))
        .where(User.id == target_user_id)
    )
    target: User | None = target_result.scalar_one_or_none()
    if not target:
        return None

    tags = [us.subject.name for us in target.user_subjects if us.subject]
    avatar = target.profile.avatar_url if target.profile else None

    return MatchResult(
        user_id=target.id,
        full_name=target.full_name,
        university=target.university,
        major=target.major,
        gpa=float(target.gpa) if target.gpa else None,
        avatar_url=avatar,
        tags=tags[:5],
        score=score.total_score,
        factors=FactorBreakdown(
            subject_score=score.subject_score,
            schedule_score=score.schedule_score,
            style_score=score.style_score,
            goal_score=score.goal_score,
            gpa_score=score.gpa_score,
        ),
        status="suggested",
    )


async def send_connect_request(
    current_user: User, target_user_id: UUID, db: AsyncSession
) -> Match:
    """Upsert a Match row with status='pending' (or 'connected' if mutual)."""
    # canonical ordering
    uid_a = min(current_user.id, target_user_id)
    uid_b = max(current_user.id, target_user_id)

    result = await db.execute(
        select(Match).where(Match.user_id_a == uid_a, Match.user_id_b == uid_b)
    )
    match: Match | None = result.scalar_one_or_none()

    if match is None:
        # Compute score for storage
        query_input = await _load_feature_input(current_user.id, db)
        target_input = await _load_feature_input(target_user_id, db)
        score_obj = (
            recommender.score_pair(query_input, target_input)
            if query_input and target_input
            else None
        )
        match = Match(
            user_id_a=uid_a,
            user_id_b=uid_b,
            score=score_obj.total_score if score_obj else 0.0,
            subject_score=score_obj.subject_score if score_obj else None,
            schedule_score=score_obj.schedule_score if score_obj else None,
            style_score=score_obj.style_score if score_obj else None,
            goal_score=score_obj.goal_score if score_obj else None,
            gpa_score=score_obj.gpa_score if score_obj else None,
            status="pending",
            initiated_by=current_user.id,
        )
        db.add(match)
    else:
        # If the other party already sent a request → mark connected
        if match.status == "pending" and match.initiated_by != current_user.id:
            match.status = "connected"
        elif match.status == "suggested":
            match.status = "pending"
            match.initiated_by = current_user.id

    return match