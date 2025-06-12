from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import SQLAlchemyError
from database.mysql import AsyncSessionLocal
from common.context_store import db_session_var


class DBSessionMiddleware(BaseHTTPMiddleware):
    """요청-전체 트랜잭션을 관리하는 세션 미들웨어."""

    async def dispatch(self, request: Request, call_next):
        async with AsyncSessionLocal() as session:
            token = db_session_var.set(session)
            try:
                response = await call_next(request)
                await session.commit()
                return response
            except SQLAlchemyError:
                await session.rollback()
                raise
            finally:
                db_session_var.reset(token)
