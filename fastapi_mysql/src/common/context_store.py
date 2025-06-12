from contextvars import ContextVar
from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

# 요청 추적용
request_id_var: ContextVar[str] = ContextVar(
    "request_id_var",
    default=str(uuid.uuid4()),
)

# DB 세션 보관용
db_session_var: ContextVar[Optional[AsyncSession]] = ContextVar(
    "db_session_var",
    default=None,
)

# 유저 세션 보관용
user_context: ContextVar[Optional[str]] = ContextVar(
    "user",
    default="Anonymous",
)
