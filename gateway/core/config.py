from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "LLM Security Gateway"
    APP_VERSION: str = "1.0.0"
    INTEGRATION_MODE: str = "local"

    LOG_LEVEL: str = "INFO"

    THREAT_ENGINE_URL: str = "http://localhost:8001"
    RISK_ENGINE_URL: str = "http://localhost:8002"

    ENABLE_REQUEST_LOGGING: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()