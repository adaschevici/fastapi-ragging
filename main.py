from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import bootstrap
from config import get_settings
from routes import router as api_router


def create_app():
    config = get_settings()
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_HOST_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", bootstrap.create_start_app_handler(app))
    app.add_event_handler("shutdown", bootstrap.create_stop_app_handler(app))

    app.include_router(api_router, prefix="/api")

    return app

app = create_app()

