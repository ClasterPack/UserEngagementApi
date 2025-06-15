import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",  # Allow extra fields
    )
    debug: bool = Field(default=False, alias="DEBUG")
    project_name: str = Field(default="UserEngagement", alias="PROJECT_NAME")
    """Mongo DB"""
    mongo_url: str = Field(default="mongodb://localhost:27017", alias="MONGO_URL")

settings = Settings()
