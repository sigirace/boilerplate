import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from common.context_store import request_id_var


class XSessionIdMiddleware(BaseHTTPMiddleware):
    """클라이언트가 보내온 X-Session-ID 헤더를 유지하거나 자동 생성한다."""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Session-ID", str(uuid.uuid4()))
        token = request_id_var.set(request_id)  # ContextVar에 보관
        try:
            response = await call_next(request)
            response.headers["X-Session-ID"] = request_id
            return response
        finally:
            request_id_var.reset(token)
