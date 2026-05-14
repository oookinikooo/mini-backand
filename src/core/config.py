from pathlib import Path
from urllib.parse import quote_plus

from dotenv import find_dotenv
from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(), env_file_encoding="utf-8", extra="ignore"
    )

    BOT_TOKEN: str
    LOG_CHAT_ID: int
    TOPIC_ID: int | None = None

    JWT_SECRET_KEY: str
    JWT_ALG: str

    AD_LOGIN: str
    AD_PASSWORD: str

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str

    @property
    def POSTGRES_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=quote_plus(self.POSTGRES_PASSWORD.get_secret_value()),
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


config = Settings()
