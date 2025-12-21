from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # CORS Settings
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()
