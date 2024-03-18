import os
from functools import lru_cache
from pydantic import Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="config.env", env_file_encoding="utf-8")
    hf_access_token: SecretStr = Field(alias="HUGGINGFACEHUB_API_TOKEN")
    openai_api_key: SecretStr = Field(alias="OPENAI_API_KEY")
    qdrant_host: str = Field(default="localhost", alias="QDRANT_HOST")
    qdrant_port: int = Field(default=6333, alias="QDRANT_PORT")
    PROJECT_NAME: str = Field(default="integration", alias="PROJECT_NAME")
    VERSION: str = Field(default="0.1.0", alias="PROJECT_VERSION")
    ALLOWED_HOST_ORIGINS: str = Field(default="*", alias="ALLOWED_HOST_ORIGINS")

    @computed_field
    @property
    def qdrant_host_port(self) -> str:
        return f"http://{self.qdrant_host}:{self.qdrant_port}"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = settings.hf_access_token.get_secret_value()
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key.get_secret_value()
    return settings
