from typing import List, Tuple
from sqlalchemy import delete, func, select
from domain.user.user_repo import IUserRepository
from domain.user.user import User as UserVO
from infra.user.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from infra.user.user_mapper import UserInfraMapper


class UserRepositoryImpl(IUserRepository):

    async def get(
        self,
        id: str,
        session: AsyncSession,
    ) -> UserVO | None:
        stmt = select(User).where(User.id == id)
        result = await session.execute(stmt)
        orm_user = result.scalar_one_or_none()

        return UserInfraMapper.to_vo(orm_user) if orm_user else None

    async def list(
        self,
        page: int,
        item_per_page: int,
        session: AsyncSession,
    ) -> Tuple[int, List[UserVO]]:
        offset = (page - 1) * item_per_page

        total_stmt = select(func.count()).select_from(User)
        total_result = await session.execute(total_stmt)
        total_count = total_result.scalar()

        stmt = select(User).offset(offset).limit(item_per_page)
        result = await session.execute(stmt)
        users = result.scalars().all()

        user_vos = [UserInfraMapper.to_vo(user) for user in users]

        return total_count, user_vos

    async def save(
        self,
        entity: UserVO,
        session: AsyncSession,
    ) -> None:
        new_user = UserInfraMapper.to_orm_model(entity)
        session.add(new_user)

    async def get_by_email(
        self,
        email: str,
        session: AsyncSession,
    ) -> UserVO | None:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        orm_user = result.scalar_one_or_none()

        return UserInfraMapper.to_vo(orm_user) if orm_user else None

    async def delete(
        self,
        id: str,
        session: AsyncSession,
    ) -> None:
        stmt = delete(User).where(User.id == id)
        await session.execute(stmt)
