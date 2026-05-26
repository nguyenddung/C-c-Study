"""
Group service — business logic for study group management.

Extracted from the route layer so it can be unit-tested and reused.
"""

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.group import GroupMember, StudyGroup
from app.models.notification import Notification
from app.models.user import User


async def get_member_count(group_id: UUID, db: AsyncSession) -> int:
    """Return the current member count for *group_id*."""
    result = await db.execute(
        select(func.count()).select_from(GroupMember).where(GroupMember.group_id == group_id)
    )
    return result.scalar_one()


async def get_group_or_404(group_id: UUID, db: AsyncSession) -> StudyGroup:
    """Fetch a group by PK or raise 404."""
    result = await db.execute(
        select(StudyGroup).where(StudyGroup.id == group_id)
    )
    group = result.scalar_one_or_none()
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "GROUP_NOT_FOUND", "message": f"Group {group_id} not found"},
        )
    return group


async def user_is_member(group_id: UUID, user_id: UUID, db: AsyncSession) -> bool:
    """Return True if *user_id* is a member of *group_id*."""
    result = await db.execute(
        select(GroupMember).where(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id,
        )
    )
    return result.scalar_one_or_none() is not None


async def get_group_with_count(
    group_id: UUID, db: AsyncSession
) -> tuple[StudyGroup, int]:
    """Return (group, member_count) tuple, raising 404 if not found."""
    group = await get_group_or_404(group_id, db)
    count = await get_member_count(group_id, db)
    return group, count


async def add_member(
    group: StudyGroup,
    user: User,
    db: AsyncSession,
    role: str = "member",
) -> GroupMember:
    """
    Add *user* to *group* as *role*.

    Checks for duplicate membership and group capacity before inserting.
    Sends a notification to the group owner on join.

    Raises:
        409 if already a member.
        400 if the group is at capacity.
    """
    if await user_is_member(group.id, user.id, db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "ALREADY_MEMBER", "message": "You are already in this group"},
        )

    count = await get_member_count(group.id, db)
    if count >= group.max_members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "GROUP_FULL", "message": "This group has reached its member limit"},
        )

    member = GroupMember(group_id=group.id, user_id=user.id, role=role)
    db.add(member)

    # Notify group owner (skip if user IS the owner)
    if group.owner_id != user.id:
        db.add(Notification(
            user_id=group.owner_id,
            type="group_join",
            title=f"{user.full_name} đã tham gia nhóm {group.name}",
            data={"group_id": str(group.id), "user_id": str(user.id)},
        ))

    await db.flush()
    return member


async def remove_member(
    group: StudyGroup,
    user: User,
    db: AsyncSession,
) -> None:
    """
    Remove *user* from *group*.

    Raises:
        404 if the user is not a member.
        400 if the user is the owner (must transfer first).
    """
    result = await db.execute(
        select(GroupMember).where(
            GroupMember.group_id == group.id,
            GroupMember.user_id == user.id,
        )
    )
    member = result.scalar_one_or_none()

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_A_MEMBER", "message": "You are not a member of this group"},
        )
    if member.role == "owner":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "OWNER_CANNOT_LEAVE",
                "message": "Transfer ownership to another member before leaving",
            },
        )

    await db.delete(member)