import os


class Settings(object):
    port = 8000

    # POSTGRESQL_USER: str = os.getenv("POSTGRESQL_USER")
    # POSTGRESQL_PASSWORD: str = os.getenv("POSTGRESQL_PASSWORD")
    # POSTGRESQL_SERVER: str = os.getenv("POSTGRESQL_SERVER")
    # POSTGRESQL_PORT: str = os.getenv("POSTGRESQL_PORT")
    # POSTGRESQL_DATABASE: str = os.getenv("POSTGRESQL_DATABASE")
    POSTGRESQL_USER: str = 'postgres'
    POSTGRESQL_PASSWORD: str = '911911'
    POSTGRESQL_SERVER: str = 'localhost'
    POSTGRESQL_PORT: str = '5432'
    POSTGRESQL_DATABASE: str = 'postgres'
    POSTGRESQL_DATABASE_URI = f'postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_SERVER}:{POSTGRESQL_PORT}/{POSTGRESQL_DATABASE}'

    # SECRET_KEY = os.getenv("SECRET_KEY")
    SECRET_KEY = '025b376adf584b72888bffe69f90524d'
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    class Config:
        env_file = "local.env"
