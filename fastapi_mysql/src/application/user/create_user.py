from application.service.validate_service import ValidateService
from domain.user.user_repo import IUserRepository
from domain.user.user import User
from common.except_handler import handle_exceptions
from utils.crypto import Crypto
from sqlalchemy.ext.asyncio import AsyncSession
from logs.log_wrapper import StructuredLogger
import logging


logger = StructuredLogger(logging.getLogger(__name__))


class CreateUser:

    def __init__(
        self,
        user_repo: IUserRepository,
        validate_service: ValidateService,
        crypt: Crypto,
    ):
        self.user_repo = user_repo
        self.validate_service = validate_service
        self.crypt = crypt

    @handle_exceptions
    async def __call__(
        self,
        name: str,
        email: str,
        password: str,
        session: AsyncSession,
    ) -> User:

        logger.info("[START] Signup Process", name=name, email=email, password=password)

        await self.validate_service.email_duplicate_check(
            email=email,
            session=session,
        )

        user = User.create(
            name=name,
            email=email,
            password=self.crypt.encrypt(password),
        )

        await self.user_repo.save(
            entity=user,
            session=session,
        )
        logger.info(f"[SUCCESS] User Created")

        logger.info(f"[END] Signup Process")

        return user
