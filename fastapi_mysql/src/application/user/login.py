from typing import Tuple
from application.service.validate_service import ValidateService
from sqlalchemy.ext.asyncio import AsyncSession

from domain.user.exceptions import NotAuthorized
from utils.crypto import Crypto
from utils.jwt import JWT
from common.except_handler import handle_exceptions
from logs.log_wrapper import StructuredLogger
import logging


logger = StructuredLogger(logging.getLogger(__name__))


class Login:

    def __init__(
        self,
        validate_service: ValidateService,
        crypt: Crypto,
        jwt: JWT,
    ):
        self.validate_service = validate_service
        self.crypt = crypt
        self.jwt = jwt

    @handle_exceptions
    async def __call__(
        self,
        email: str,
        password: str,
        session: AsyncSession,
    ) -> Tuple[str, str]:
        logger.info(f"[START] Login Process", email=email)

        user = await self.validate_service.user_validate_by_email(
            email=email,
            session=session,
        )

        if not self.crypt.verify(password, user.password):
            raise NotAuthorized(
                email=email,
            )

        logger.info(f"[SUCCESS] User Login")

        payload = {
            "sub": user.id,
            "email": user.profile.email,
        }

        access_token = self.jwt.create_access_token(payload=payload)
        refresh_token = self.jwt.create_refresh_token(payload=payload)

        logger.info(f"[SUCCESS] Publish Token")

        logger.info(f"[END] Login Process")

        return (
            access_token,
            refresh_token,
        )
