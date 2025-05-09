from pydantic import EmailStr, ConfigDict
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    POSTGRES_USER: str = 'abc'
    POSTGRES_PASSWORD: str = 'abc'
    POSTGRES_DB: str = 'abc'
    POSTGRES_PORT: int = 5432
    POSTGRES_DOMAIN: str = 'localhost'

    DB_URL: str = 'postgresql+asyncpg://abc:abc@localhost:5432/abc'

    REDIS_PORT: int = 6379
    REDIS_HOST: str = 'localhost'
    REDIS_PASSWORD: str | None = None

    MAIL_USERNAME: EmailStr = 'test@meta.ua'
    MAIL_PASSWORD: str = '12345678'
    MAIL_PORT: int = 465
    MAIL_SERVER: str = 'smtp.some.ua'

    JWT_SECRET_KEY: str = 'secret_key'
    JWT_ALGORITHM: str = 'HS256'

    CLOUDINARY_CLOUD_NAME: str = 'abc'
    CLOUDINARY_API_KEY: str = 'abc'
    CLOUDINARY_API_SECRET: str = 'abc'

    model_config = ConfigDict(extra='ignore', env_file='.env', env_file_encoding='utf-8')


config = Config()
