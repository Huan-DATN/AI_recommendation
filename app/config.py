import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URL = os.getenv(
        "DB_URL", "postgresql+psycopg2://postgres:postgres@localhost:5444/wedding"
    )

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    REDIS_DB = os.getenv("REDIS_DB", 0)


def get_config():
    """Get the configuration object."""
    return Config()
