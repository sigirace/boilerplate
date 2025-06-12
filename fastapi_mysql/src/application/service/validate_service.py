from domain.user.exceptions import EmailAlreadyExists, UserNotFound
from domain.user.user_repo import IUserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from domain.user.user import User
from logs.log_wrapper import StructuredLogger
import logging


logger = StructuredLogger(logging.getLogger(__name__))


class ValidateService:

    def __init__(
        self,
        user_repo: IUserRepository,
    ):
        self.user_repo = user_repo

    async def user_validate_by_id(
        self,
        user_id: str,
        session: AsyncSession,
    ) -> User:

        logger.info(f"[START] user validate by id process", user_id=user_id)

        user = await self.user_repo.get(
            id=user_id,
            session=session,
        )

        if not user:
            logger.error(f"[ERROR] user not founded by id")
            raise UserNotFound(user_id)

        logger.info(f"[END] user validate by id process")

        return user

    async def user_validate_by_email(
        self,
        email: str,
        session: AsyncSession,
    ) -> User | None:

        logger.info(f"[START] user validate by email process", email=email)

        user = await self.user_repo.get_by_email(
            email=email,
            session=session,
        )

        if not user:
            logger.error(f"[ERROR] user not founded by email")
            raise UserNotFound(email)

        logger.info(f"[END] user validate by email process")

        return user

    async def email_duplicate_check(
        self,
        email: str,
        session: AsyncSession,
    ):

        logger.info(f"[START] email duplicate check process", email=email)

        user = await self.user_repo.get_by_email(
            email=email,
            session=session,
        )

        if user:
            logger.info(f"[ERROR] email already exist")
            raise EmailAlreadyExists(email)

        logger.info(f"[END] email duplicate check process")
