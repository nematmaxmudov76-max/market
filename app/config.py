from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_VERSION: str = "v1"
    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str = "Ilovada sotuv, sotib olish, kuryer bo'lish imkoni bor"
    
    # for session auth
    SESSION_EXPIRATION_DAY: int = 7
    
    # for jwt auth
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 
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
    REDIS_URL:str
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"


    # EMAIL SETTINGS
    EMAIL_FROM: str = "nematmaxmudov76@gmail.com"
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT:int = 587
    EMAIL_PASSWORD:str 
    # Pydantic v2 uchun yangi config va kutilmagan extra o'zgaruvchilarni e'tiborsiz qoldirish
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()



# Autentifikatsiya talab qilinmaydigan ochiq API yo'llari
EXCLUDE_PATHS = {
    "/api/v1/auth/login",
    "/api/v1/auth/logout",
    "/api/v1/auth/register",
    "/api/v1/jwt/login",
    "/api/v1/session/login",
    "/api/v1/user-register",
    "/api/v1/user-register/verify/{secret_code}",
    "/api/v1/user/get_users",



    # HOME Page uchun, hali login qilmagan foydalanuvchi uchun
    "/api/v1/home/search-by-name",
    "/api/v1/home/search-by-category",
    "/api/v1/home/discount-products",
    "/api/v1/home/liked-products",
    "/api/v1/home/monthly-discount",
    "/api/v1/home/top-10-products",
    "/api/v1/home/user-top-products"
}