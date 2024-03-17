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
