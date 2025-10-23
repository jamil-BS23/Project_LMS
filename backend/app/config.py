# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20000000
    MAX_BORROW_LIMIT: int = 5
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    JWT_EXPIRATION_MINUTES: int = 60  

    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str = "media"


    class Config:
        env_file = ".env"
        extra = "allow"

# Initialize settings
settings = Settings()





