from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DbSettings(BaseSettings):
    """Настройки базы данных."""

    url: str = "sqlite+aiosqlite:///germany_goods.db"
    echo: bool = True


class ApiAuthSettings(BaseSettings):
    username: str = ""
    password: str = ""

    class Config:
        env_prefix = "APP__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    api_auth: ApiAuthSettings = ApiAuthSettings()
    db: DbSettings = DbSettings()


settings = Settings()
