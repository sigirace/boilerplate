from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.types import ASGIApp, Scope, Receive, Send
from starlette.requests import Request
from common.context_store import user_context

from utils.jwt import JWT

import logging

logger = logging.getLogger(__name__)


class AuthMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        jwt: JWT,
    ):
        self.app = app
        self.jwt = jwt

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ):

        logger.info("[START] get auth from header")
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(
            scope=scope,
            receive=receive,
        )

        try:
            authorization = request.headers.get("Authorization")

            if authorization:
                splits = authorization.split(" ")
                if splits[0] == "Bearer":
                    token = splits[1]
                    payload = self.jwt.decode_token(token)
                    user_id = payload.get("sub")

                    user_context.set(user_id)
                    logger.info("[SUCCESS] set user id in contextvar")
                else:
                    logger.info("[FAIL] no bearer token in header")
            else:
                logger.info("[FAIL] no authorization in header")

            await self.app(scope, receive, send)

        except HTTPException as e:
            logger.error(f"[ERROR] error occured by {str(e)}")
            response = JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )
            await response(scope, receive, send)
