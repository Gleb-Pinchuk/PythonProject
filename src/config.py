import os
from dotenv import load_dotenv

load_dotenv()


def load_db_config():
    """
    Возвращает параметры подключения к PostgreSQL (без имени базы данных).
    Выбрасывает исключение, если обязательные переменные не заданы.
    """
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD")

    if not password:
        raise ValueError("Переменная окружения DB_PASSWORD не задана. Проверьте файл .env.")

    return {
        "host": host,
        "user": user,
        "password": password,
    }


def get_db_name() -> str:
    """Возвращает имя целевой базы данных."""
    db_name = os.getenv("DB_NAME", "hh_vacancies")
    if not db_name.strip():
        raise ValueError("Имя базы данных (DB_NAME) не может быть пустым.")
    return db_name
