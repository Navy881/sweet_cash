import os
from dotenv import load_dotenv
from pydantic.types import PositiveInt


load_dotenv(os.path.join('local.env'))


class Settings(object):
    port: int = int(os.getenv("APP_PORT"))

    POSTGRESQL_USER: str = os.getenv("POSTGRESQL_USER")
    POSTGRESQL_PASSWORD: str = os.getenv("POSTGRESQL_PASSWORD")
    POSTGRESQL_SERVER: str = os.getenv("POSTGRESQL_SERVER")
    POSTGRESQL_PORT: str = os.getenv("POSTGRESQL_PORT")
    POSTGRESQL_DATABASE: str = os.getenv("POSTGRESQL_DATABASE")
    POSTGRESQL_DATABASE_URI: str = f'postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_SERVER}:{POSTGRESQL_PORT}/{POSTGRESQL_DATABASE}'
    POSTGRESQL_POOL_SIZE: PositiveInt = 10
    POSTGRESQL_CONNECTION_TIMEOUT: PositiveInt = 60

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 1400

    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: str = os.getenv("REDIS_PORT")
    REDIS_DB: str = os.getenv("REDIS_DB")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")
    REDIS_DSN: str = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
    TRANSACTIONS_CATEGORIES_CACHE_TTL_SECOND = 600

    NALOG_RU_HOST: str = os.getenv("NALOG_RU_HOST")
    NALOG_RU_CLIENT_SECRET: str = os.getenv("NALOG_RU_CLIENT_SECRET")
    NALOG_RU_OS: str = os.getenv("NALOG_RU_OS")
    NALOG_RU_DEVICE_OS: str = os.getenv("NALOG_RU_DEVICE_OS")
    NALOG_RU_DEVICE_ID: str = os.getenv("NALOG_RU_DEVICE_ID")
    NALOG_RU_TIMEOUT: float = 600

    EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PHONE_REGEX = r'^((\+7)+([0-9]){10})$'
    PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

    MIN_TRANSACTION_AMOUNT = 0
    MAX_TRANSACTION_AMOUNT = 999999999999

    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: int = os.getenv("SMTP_PORT")
    EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")

    JWT_EXPIRE_TIME = 24

    DEBUG = os.getenv("DEBUG")

    EVENT_PROCESSORS = ['Processor-1']
    EVENT_LISTENING_PERIOD_IN_SECONDS = 10

    SIZE_POOL_AIOHTTP = 100

    HOST = os.getenv("HOST")

    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_SECURITY_PROTOCOL: str = os.getenv("KAFKA_SECURITY_PROTOCOL")
    KAFKA_SASL_MECHANISM: str = os.getenv("KAFKA_SASL_MECHANISM")
    KAFKA_SASL_PLAIN_USERNAME: str = os.getenv("KAFKA_SASL_PLAIN_USERNAME")
    KAFKA_SASL_PLAIN_PASSWORD: str = os.getenv("KAFKA_SASL_PLAIN_PASSWORD")

    MAX_USER_TOKENS: int = 5

    CURRENCIES = {
        "USD": "Доллар США",
        "EUR": "Евро",
        "RUB": "Российский рубль",
        "JPY": "Японская иена",
        "GBP": "Британский фунт стерлингов",
        "AUD": "Австралийский доллар",
        "CAD": "Канадский доллар",
        "CHF": "Швейцарский франк",
        "CNY": "Китайский юань",
        "SEK": "Шведская крона",
        "NZD": "Новозеландский доллар",
        "MXN": "Мексиканское песо",
        "SGD": "Сингапурский доллар",
        "HKD": "Гонконгский доллар",
        "NOK": "Норвежская крона",
        "KRW": "Южнокорейская вона",
        "TRY": "Турецкая лира",
        "INR": "Индийская рупия",
        "BRL": "Бразильский реал",
        "ZAR": "Южноафриканский рэнд",
        "PLN": "Польский злотый",
        "DKK": "Датская крона",
        "AED": "Дирхам ОАЭ",
        "SAR": "Саудовский риял",
        "THB": "Таиландский бат",
        "IDR": "Индонезийская рупия",
        "MYR": "Малайзийский ринггит",
        "PHP": "Филиппинское песо",
        "CZK": "Чешская крона",
        "HUF": "Венгерский форинт",
        "ILS": "Израильский новый шекель",
        "CLP": "Чилийское песо",
        "COP": "Колумбийское песо",
        "PEN": "Перуанский соль",
        "EGP": "Египетский фунт",
        "VND": "Вьетнамский донг",
        "NGN": "Нигерийская найра",
        "PKR": "Пакистанская рупия",
        "BDT": "Бангладешская така",
        "UAH": "Украинская гривна",
        "QAR": "Катарский риял",
        "KZT": "Казахстанский тенге",
    }

    class Config:
        env_file = "local.env"
