import logging
from fastapi import HTTPException, status
from functools import wraps
import asyncio


def handle_exceptions(func):

    logger = logging.getLogger(func.__module__)

    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                response = await func(*args, **kwargs)
                return response
            except HTTPException as e:
                logger.exception(
                    f"[EXCEPTION] Unhandled exception in {func.__qualname__}\ndetail:{str(e)}"
                )
                raise
            except Exception as e:
                logger.exception(
                    f"[EXCEPTION] Unhandled exception in {func.__qualname__}\ndetail:{str(e)}"
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e),
                )

        return wrapper
    else:

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                return response
            except HTTPException as e:
                logger.exception(
                    f"[EXCEPTION] Unhandled exception in {func.__qualname__}\ndetail:{str(e)}"
                )
                raise
            except Exception as e:
                logger.exception(
                    f"[EXCEPTION] Unhandled exception in {func.__qualname__}\ndetail:{str(e)}"
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e),
                )

        return wrapper
