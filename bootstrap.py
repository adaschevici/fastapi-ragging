from functools import lru_cache
from typing import Callable
from fastapi import FastAPI
from starlette.requests import Request
from app_logging import logger

from tasks.log_handling import setup_logging, teardown_logging
from tasks.qdrant_handling import setup_qdrant, teardown_qdrant


async def noop_setup(*args, **kwargs):
    return


async def noop_teardown(*args, **kwargs):
    return


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await setup_logging(app)
        await setup_qdrant(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await teardown_logging(app)
        await teardown_qdrant(app)

    return stop_app

@lru_cache
def get_logger(request: Request = None):
    if request is None:
        return logger
    return request.app.state._logger

