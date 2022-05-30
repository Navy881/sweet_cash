import os
from dotenv import load_dotenv


load_dotenv(os.path.join('local.env'))


class Settings(object):
    port = 5000

    POSTGRESQL_USER: str = os.getenv("POSTGRESQL_USER")
    POSTGRESQL_PASSWORD: str = os.getenv("POSTGRESQL_PASSWORD")
    POSTGRESQL_SERVER: str = os.getenv("POSTGRESQL_SERVER")
    POSTGRESQL_PORT: str = os.getenv("POSTGRESQL_PORT")
    POSTGRESQL_DATABASE: str = os.getenv("POSTGRESQL_DATABASE")
    POSTGRESQL_DATABASE_URI = f'postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_SERVER}:{POSTGRESQL_PORT}/{POSTGRESQL_DATABASE}'

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    REDIS_DB: int = os.getenv("REDIS_DB")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")

    NALOG_RU_HOST: str = os.getenv("NALOG_RU_HOST")
    NALOG_RU_CLIENT_SECRET: str = os.getenv("NALOG_RU_CLIENT_SECRET")
    NALOG_RU_OS: str = os.getenv("NALOG_RU_OS")
    NALOG_RU_DEVICE_OS: str = os.getenv("NALOG_RU_DEVICE_OS")
    NALOG_RU_DEVICE_ID: str = os.getenv("NALOG_RU_DEVICE_ID")

    EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PHONE_REGEX = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

    MIN_TRANSACTION_AMOUNT = 0
    MAX_TRANSACTION_AMOUNT = 999999999999

    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: int = os.getenv("SMTP_PORT")
    EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")

    JWT_EXPIRE_TIME = 24

    DEBUG = True

    EVENT_PROCESSORS = ['Processor-1']
    EVENT_LISTENING_PERIOD_IN_SECONDS = 10

    SIZE_POOL_AIOHTTP = 100

    class Config:
        env_file = "local.env"
