# common/log_handler.py
import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from configs import get_settings
from common.context_store import user_context, request_id_var

LOG_COL = get_settings().mongo.mongodb_log_col


class MotorLogHandler(logging.Handler):
    """Motor 비동기 MongoDB 로그 핸들러 (TTL 인덱스 자동 관리)"""

    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        level: int | str = logging.INFO,
        retention_days: Optional[int] = 30,
    ):
        super().__init__(level)
        self.loop = asyncio.get_running_loop()  # 현재 실행 중인 루프 고정
        self.coll: AsyncIOMotorCollection = db[LOG_COL]

        if retention_days:
            expire_seconds = retention_days * 24 * 3600
            self.loop.create_task(self._ensure_ttl_index(expire_seconds))

    # ---------- private ----------
    async def _ensure_ttl_index(self, expire_seconds: int) -> None:
        indexes = await self.coll.index_information()
        if not any(
            "created_at" in [f for f, _ in spec["key"]] for spec in indexes.values()
        ):
            await self.coll.create_index(
                [("created_at", 1)],
                expireAfterSeconds=expire_seconds,
                background=True,
            )

    def _format_record(self, record: logging.LogRecord) -> Dict[str, Any]:
        return {
            "logger": record.name,
            "level": record.levelname,
            "req_id": request_id_var.get(),
            "user": user_context.get(),
            "msg": record.getMessage(),
            "pathname": record.pathname,
            "lineno": record.lineno,
            "funcName": record.funcName,
            "created_at": datetime.now(timezone.utc),
            "module": record.module,
            "process": record.processName,
            "thread": record.threadName,
            "extra": record.__dict__.get("extra", {}),
        }

    async def _insert(self, doc: Dict[str, Any]) -> None:
        try:
            await self.coll.insert_one(doc)
        except Exception as e:
            # 콘솔 경고용 (여기에 다시 MotorLogHandler 가 달려있어도 recursion 없음)
            logging.getLogger(__name__).warning("Mongo log insert failed: %s", e)

    # ---------- logging.Handler 구현 ----------
    def emit(self, record: logging.LogRecord) -> None:  # type: ignore[override]
        try:
            doc = self._format_record(record)
            self.loop.create_task(self._insert(doc))
        except Exception:
            self.handleError(record)

    async def close_async(self) -> None:
        await super().close()  # noop

    def close(self) -> None:
        try:
            super().close()
        except Exception:
            pass
