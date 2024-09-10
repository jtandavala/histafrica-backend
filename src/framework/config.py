from pathlib import Path
from typing import Dict
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)  # Modern Pydantic settings
from pydantic import Field, field_validator
import os
import dj_database_url

# Define the path to the environment folder
_ENV_FOLDER = Path(__file__).resolve().parent.parent.parent / "envs"

# Get the current environment (development, production, etc.)
APP_ENV = os.getenv("APP_ENV")  # Where to pass the APP_ENV value


class ConfigService(BaseSettings):

    database_dsn: str
    database_conn: Dict = Field(init=False, default=None)
    debug: bool = False
    language_code: str = "en-us"
    secret_key: str
    test_keep_db: bool = True
    test_use_migrations: bool = True

    model_config = SettingsConfigDict(
        env_file=[f"{_ENV_FOLDER}/.env", f"{_ENV_FOLDER}/.env.{APP_ENV}"],
    )

    @field_validator("database_conn", mode="before")
    def make_database_conn(cls, v, info):
        return dj_database_url.config(default=info.data["database_dsn"])

    @field_validator("debug", mode="before")
    def parse_debug(cls, v):
        if isinstance(v, str):
            return v.lower() == "true"
        return v

    @field_validator("test_keep_db", mode="before")
    def parse_test_keep_db(cls, v):
        if isinstance(v, str):
            return v.lower() == "true"
        return v

    @field_validator("test_use_migrations", mode="before")
    def parse_test_use_migration(cls, v):
        if isinstance(v, str):
            return v.lower() == "true"
        return v


# Initialize the configuration service
config_service = ConfigService()
