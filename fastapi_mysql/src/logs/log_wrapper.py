import logging
from typing import Any


class StructuredLogger:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def info(self, msg: str, **extra_fields: Any):
        self.logger.info(msg, extra={"extra": extra_fields})

    def warning(self, msg: str, **extra_fields: Any):
        self.logger.warning(msg, extra={"extra": extra_fields})

    def error(self, msg: str, **extra_fields: Any):
        self.logger.error(msg, extra={"extra": extra_fields})

    def debug(self, msg: str, **extra_fields: Any):
        self.logger.debug(msg, extra={"extra": extra_fields})
