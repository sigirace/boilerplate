from domain.user.user_repo import IUserRepository
from sqlalchemy.ext.asyncio import AsyncSession

from domain.user.user import UserList
from common.except_handler import handle_exceptions
from logs.log_wrapper import StructuredLogger
import logging


logger = StructuredLogger(logging.getLogger(__name__))


class GetListUsers:

    def __init__(
        self,
        user_repo: IUserRepository,
    ):
        self.user_repo = user_repo

    @handle_exceptions
    async def __call__(
        self,
        page: int,
        item_per_page: int,
        session: AsyncSession,
    ) -> UserList:

        logger.info(
            f"[START] Get User List Process", page=page, item_per_page=item_per_page
        )

        total_count, users = await self.user_repo.list(
            page=page,
            item_per_page=item_per_page,
            session=session,
        )

        logger.info(f"[SUCCESS] Get User List Process")

        logger.info(f"[END] Get User List Process")

        return UserList(
            total_count=total_count,
            page=page,
            users=users,
        )
