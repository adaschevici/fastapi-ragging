import os
from functools import lru_cache
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="config.env", env_file_encoding="utf-8")
    hf_access_token: SecretStr = Field(alias="HUGGINGFACEHUB_API_TOKEN")
    openai_api_key: SecretStr = Field(alias="OPENAI_API_KEY")
    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = settings.hf_access_token.get_secret_value()
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key.get_secret_value()
    return settings
