from typing import Callable
from fastapi import FastAPI

from tasks.log_handling import setup_logging, teardown_logging


async def noop_setup(*args, **kwargs):
    return


async def noop_teardown(*args, **kwargs):
    return


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await setup_logging(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await teardown_logging(app)

    return stop_app

