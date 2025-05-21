from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    db_user: str = "postgres"
    db_pass: str = "postgres"
    db_name: str = ""
    db_host: str = "localhost"
    db_port: int = 5432
    openai_api_key: str = ""
    

    model_config = SettingsConfigDict(env_file=".env.local")

def settings():
    return Settings()