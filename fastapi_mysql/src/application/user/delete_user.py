from application.service.validate_service import ValidateService
from domain.user.user_repo import IUserRepository
from common.except_handler import handle_exceptions
from sqlalchemy.ext.asyncio import AsyncSession
from logs.log_wrapper import StructuredLogger
import logging


logger = StructuredLogger(logging.getLogger(__name__))


class DeleteUser:

    def __init__(
        self,
        user_repo: IUserRepository,
        validate_service: ValidateService,
    ):
        self.user_repo = user_repo
        self.validate_service = validate_service

    @handle_exceptions
    async def __call__(
        self,
        user_id: str,
        session: AsyncSession,
    ) -> None:

        logger.info(f"[START] Delte User Process", user_id=user_id)

        existing_user = await self.validate_service.user_validate_by_id(
            user_id=user_id,
            session=session,
        )

        await self.user_repo.delete(
            id=existing_user.id,
            session=session,
        )

        logger.info(f"[END] User Deleted")

        logger.info(f"[END] Delte User Process")
