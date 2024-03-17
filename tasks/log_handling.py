from fastapi import FastAPI
from app_logging import logger

async def setup_logging(app: FastAPI) -> None:
    app.state._logger = logger
    app.state._logger.info("Logging setup complete")

async def teardown_logging(app: FastAPI) -> None:
    del app.state._logger
    logger.remove()
