from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    sql_database_url: str
    mongodb_url: str
    mongodb_database: str


settings = Settings()