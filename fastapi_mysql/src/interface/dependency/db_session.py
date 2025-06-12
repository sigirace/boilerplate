from sqlalchemy.ext.asyncio import AsyncSession
from common.context_store import db_session_var


async def get_session() -> AsyncSession:
    """미들웨어에서 넣어 둔 세션을 DI 용도로 꺼낸다."""
    session = db_session_var.get()
    if session is None:  # 미들웨어 누락 시 즉시 오류
        msg = "[ERROR] DB session not found in request context."
        raise RuntimeError(msg)

    return session
