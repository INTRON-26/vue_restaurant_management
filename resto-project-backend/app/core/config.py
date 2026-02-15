from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Resto API"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./resto.db"
    BACKEND_CORS_ORIGINS: str = "http://localhost:8080"
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
