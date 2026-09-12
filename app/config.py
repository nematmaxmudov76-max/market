from pydantic_settings import BaseSettings, SettingsConfigDict


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

    #common
    DEBUG: bool
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # MEDIA
    MEDIA_PATH: str = "media"
    FILE_SIZE: int = 1024 * 1024 * 5 # 5MB
    FILE_TYPE: list[str] = [".jpg", ".png", ".jpeg"]

    # .env faylingizda bor bo'lgan va xatolik bergan o'zgaruvchilar:
    DATABASE_URL: str | None = None
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://redis:6379/0"

    # Pydantic v2 uchun yangi config va kutilmagan extra o'zgaruvchilarni e'tiborsiz qoldirish
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()