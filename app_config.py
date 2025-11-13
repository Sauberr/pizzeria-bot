import logging

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class EnvConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    TOKEN: str
    CHANNEL_ID: str
    CHANNEL_LINK: str

    CRYPTO_TOKEN: str
    STAR_PAYMENT_TOKEN: str

    DELETE_ANIMATION_URL: str = (
        "https://media.giphy.com/media/h3oEjI6SIIHBdRxXI40/giphy.gif"
    )

    RATE_API_URL: str

    ADMIN_LIST: str = Field(default="", alias="ADMIN_LIST")

    @property
    def ADMIN_USER_LIST(self) -> list[int]:
        if not self.ADMIN_LIST:
            return []
        try:
            return [
                int(admin_id)
                for admin_id in self.ADMIN_LIST.split(",")
                if admin_id.strip()
            ]
        except ValueError:
            logger.error("ADMIN_USER_IDS in .env is not a valid list of integers.")
            return []


env_config = EnvConfig()


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    POSTGRES_DB: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"

    DJANGO_SUPERUSER_USERNAME: str = "test"
    DJANGO_SUPERUSER_EMAIL: str = "test@gmail.com"
    DJANGO_SUPERUSER_PASSWORD: str = "test123!"


db_config = DatabaseConfig()
