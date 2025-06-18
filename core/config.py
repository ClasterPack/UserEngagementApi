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
    logstash: str = Field(default="localhost", alias="LOGSTASH")
    token_url: str = Field(default="fastapi:8000/token/", alias="TOKEN_URL")
    auth_service_url: str = Field(default="fastapi:8000/login", alias="AUTH_SERVICE_URL")
    """Mongo DB"""
    mongo_url: str = Field(default="mongodb://localhost:27017", alias="MONGO_URL")
    log_format: str = '{"request_id": "%(request_id)s", "asctime": \
                 "%(asctime)s", "levelname": "%(levelname)s", \
                 "name": "%(name)s", "message": "%(message)s", \
                 "host": "%(host)s", "user-agent": "%(user-agent)s", "method": "%(method)s", "path": "%(path)s", \
                 "query_params": "%(query_params)s", "status_code": "%(status_code)s"}'
    log_default_handler: list = Field(default=["console"], alias="LOG_DEFAULT_HANDLER")


settings = Settings()
