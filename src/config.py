import os

from dotenv import load_dotenv

load_dotenv()


def load_db_config():
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME", "postgres"),
    }
