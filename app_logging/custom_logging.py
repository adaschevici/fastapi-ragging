# Custom Logger Using Loguru

import os
import json
import logging
import sys
from pathlib import Path

from loguru import logger

loglevel_mapping = {
    50: "CRITICAL",
    40: "ERROR",
    30: "WARNING",
    20: "INFO",
    10: "DEBUG",
    0: "NOTSET",
}


def configure_logging():
    from asgi_correlation_id.context import correlation_id

    def correlation_id_filter(record):
        record["correlation_id"] = correlation_id.get()
        return record["correlation_id"]

    logger.remove()
    set_level = os.getenv("LOG_LEVEL", logging.INFO)
    fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS zz}</green> | <level>{level: <8}</level> | <yellow>Req ID: [{correlation_id}]</yellow> | <yellow>Line {line: >4} ({file}):</yellow> <b>{message}</b>"
    logger.add(
        "app_logging.log",
        format=fmt,
        level=set_level,
        filter=correlation_id_filter,
        rotation="1 week",
        retention="1 month",
        compression="zip",
    )
    logger.add(
        sys.stderr,
        format=fmt,
        level=set_level,
        filter=correlation_id_filter,
    )
    return logger


class InterceptHandler(logging.Handler):

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class CustomizeLogger:
    @classmethod
    def make_logger(cls, config_path: Path):
        config = cls.load_logging_config(config_path)
        logging_config = config.get("logger")
        set_level = os.getenv("LOG_LEVEL", logging_config.get("level"))

        logger = cls.customize_logging(
            logging_config.get("path"),
            level=set_level,
            retention=logging_config.get("retention"),
            rotation=logging_config.get("rotation"),
            format=logging_config.get("format"),
        )
        return logger

    @classmethod
    def customize_logging(
        cls, filepath: Path, level: str, rotation: str, retention: str, format: str
    ):
        from asgi_correlation_id import correlation_id

        logger.remove()
        logger.add(
            sys.stdout, enqueue=True, backtrace=True, level=level.upper(), format=format
        )
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            compression="zip",
            level=level.upper(),
            format=format,
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ["uvicorn", "uvicorn.error", "fastapi"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=correlation_id.get(), method=None)

    @classmethod
    def load_logging_config(cls, config_path):
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config
