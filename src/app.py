import psycopg2

from src.database import create_database
from src.hh_api import get_employers_data

EMPLOYER_IDS = [
    "1455",      # Яндекс
    "1740",      # Сбер
    "80",        # Авито
    "3529",      # Ozon
    "2180",      # VK
    "3144013",   # Тинькофф
    "84585",     # Kaspersky
    "2324020",   # Skyeng
    "39305",     # СберМаркет
    "1122462",   # Газпром нефть
]


def load_data_to_db(database_name: str, db_params: dict) -> None:
    """
    Создаёт базу данных, получает данные через API hh.ru и сохраняет их в PostgreSQL.
    """
    create_database(database_name, db_params)
    employers, vacancies = get_employers_data(EMPLOYER_IDS)

    with psycopg2.connect(dbname=database_name, **db_params) as conn:
        with conn.cursor() as cur:
            # Вставка работодателей
            for emp in employers:
                cur.execute(
                    """
                    INSERT INTO employers (employer_id, name, url)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (employer_id) DO NOTHING;
                    """,
                    (emp["employer_id"], emp["name"], emp["url"]),
                )

            for vac in vacancies:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, currency, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO NOTHING;
                    """,
                    (
                        vac["vacancy_id"],
                        vac["employer_id"],
                        vac["title"],
                        vac["salary_from"],
                        vac["salary_to"],
                        vac["currency"],
                        vac["url"],
                    ),
                )
        conn.commit()
