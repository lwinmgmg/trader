"""Configurate and Setting

Returns:
    _type_: _description_
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    """Environment Setting default to '.env' file.

    Args:
        BaseSettings (_type_): _description_
    """

    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    FUTURE_URL: str
    FUTURE_API_KEY: str
    FUTURE_SECRET: Optional[str]
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def get_env(file_path: str = ".env") -> Env:
    """Read and get environment settings for desired file path

    Args:
        file_path (str, optional): _description_. Defaults to ".env".

    Returns:
        Env: _description_
    """
    return Env(_env_file=file_path, _env_file_encoding="utf-8")
