from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from common.context_store import user_context

import logging

logger = logging.getLogger(__name__)


security = HTTPBearer()


def get_current_user(
    _: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    user_id = user_context.get()
    if user_id is None:  # 미들웨어 누락 시 즉시 오류
        msg = "[ERROR] user ud not found in request context."
        logger.error(msg=msg)
        raise RuntimeError(msg)

    logger.info("[SUCCESS] get current user")
    return user_id
