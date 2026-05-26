"""Study group routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_current_user, get_db
from app.models.group import GroupMember, StudyGroup
from app.models.user import User
from app.schemas.group import GroupCreateRequest, GroupMemberResponse, GroupResponse

router = APIRouter(prefix="/groups", tags=["groups"])


def _group_to_response(group: StudyGroup, member_count: int) -> GroupResponse:
    return GroupResponse(
        id=group.id,
        name=group.name,
        description=group.description,
        icon=group.icon,
        owner_id=group.owner_id,
        max_members=group.max_members,
        next_session=group.next_session,
        is_public=group.is_public,
        member_count=member_count,
        created_at=group.created_at,
    )


@router.get("/", response_model=list[GroupResponse])
async def list_groups(
    search: str | None = Query(None),
    limit: int = Query(20, le=50),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    stmt = select(StudyGroup).where(StudyGroup.is_public == True)  # noqa: E712
    if search:
        stmt = stmt.where(StudyGroup.name.ilike(f"%{search}%"))
    stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    groups = result.scalars().all()

    responses = []
    for g in groups:
        count_result = await db.execute(
            select(func.count()).select_from(GroupMember).where(GroupMember.group_id == g.id)
        )
        responses.append(_group_to_response(g, count_result.scalar_one()))
    return responses


@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    req: GroupCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    group = StudyGroup(
        name=req.name,
        description=req.description,
        icon=req.icon,
        subject_id=req.subject_id,
        owner_id=current_user.id,
        max_members=req.max_members,
        is_public=req.is_public,
    )
    db.add(group)
    await db.flush()
    # Owner is also a member
    db.add(GroupMember(group_id=group.id, user_id=current_user.id, role="owner"))
    return _group_to_response(group, 1)


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(select(StudyGroup).where(StudyGroup.id == group_id))
    group = result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"code": "GROUP_NOT_FOUND", "message": "Group not found"})
    count = (await db.execute(
        select(func.count()).select_from(GroupMember).where(GroupMember.group_id == group_id)
    )).scalar_one()
    return _group_to_response(group, count)


@router.post("/{group_id}/join", response_model=GroupMemberResponse, status_code=status.HTTP_201_CREATED)
async def join_group(
    group_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(StudyGroup).where(StudyGroup.id == group_id))
    group = result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail={"code": "GROUP_NOT_FOUND"})

    existing = await db.execute(
        select(GroupMember).where(
            GroupMember.group_id == group_id, GroupMember.user_id == current_user.id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail={"code": "ALREADY_MEMBER"})

    # Check capacity
    count = (await db.execute(
        select(func.count()).select_from(GroupMember).where(GroupMember.group_id == group_id)
    )).scalar_one()
    if count >= group.max_members:
        raise HTTPException(status_code=400, detail={"code": "GROUP_FULL"})

    member = GroupMember(group_id=group_id, user_id=current_user.id, role="member")
    db.add(member)
    await db.flush()
    return GroupMemberResponse(
        user_id=current_user.id,
        full_name=current_user.full_name,
        role="member",
        joined_at=member.joined_at,
    )


@router.delete("/{group_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
async def leave_group(
    group_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(GroupMember).where(
            GroupMember.group_id == group_id, GroupMember.user_id == current_user.id
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail={"code": "NOT_A_MEMBER"})
    if member.role == "owner":
        raise HTTPException(status_code=400, detail={"code": "OWNER_CANNOT_LEAVE",
                                                       "message": "Transfer ownership first"})
    await db.delete(member)


@router.get("/{group_id}/members", response_model=list[GroupMemberResponse])
async def list_members(
    group_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = await db.execute(
        select(GroupMember)
        .options(selectinload(GroupMember.user))
        .where(GroupMember.group_id == group_id)
    )
    return [
        GroupMemberResponse(
            user_id=m.user_id,
            full_name=m.user.full_name,
            role=m.role,
            joined_at=m.joined_at,
        )
        for m in result.scalars().all()
    ]