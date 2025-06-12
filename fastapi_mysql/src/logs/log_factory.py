from datetime import datetime
import logging


class MillisecondFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = datetime.fromtimestamp(record.created).strftime(datefmt)
            return s[:-3]  # 마이크로초 6자리 중 앞 3자리만 사용 (ms)
        else:
            return super().formatTime(record, datefmt)


def configure_root_logger(
    handler: logging.Handler, *, level: int = logging.INFO, to_console: bool = True
) -> None:
    root = logging.getLogger()
    root.setLevel(level)

    formatter = MillisecondFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S,%f",
    )

    handler.setFormatter(formatter)
    root.addHandler(handler)

    if to_console:
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        root.addHandler(stream)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").propagate = False
