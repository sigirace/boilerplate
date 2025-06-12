from abc import abstractmethod

from common.repository import BaseRepository
from domain.user.user import User
from sqlalchemy.ext.asyncio import AsyncSession


class IUserRepository(BaseRepository[User]):

    @abstractmethod
    async def get_by_email(
        self,
        email: str,
        session: AsyncSession,
    ) -> User | None:
        """
        이메일로 유저를 검색한다.
        """
        raise NotImplementedError
