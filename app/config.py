from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_VERSION: str = "v1"
    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str = "Ilovada sotuv, sotib olish, kuryer bo'lish imkoni bor"
    # for session auth
    SESSION_EXPIRATION_DAY: int = 7
    # for jwt auth
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    SECRET_KEY: str

    DEBUG: bool
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
