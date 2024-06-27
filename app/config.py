from pydantic_settings import BaseSettings, SettingsConfigDict
import os


DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    database_hostname: str
    database_password: str
    database_username: str
    database_port: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()
