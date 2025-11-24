import psycopg2

from src.database import create_database
from src.db_manager import DBManager
from src.hh_api import get_employers_data

EMPLOYER_IDS = [
    "1455",
    "1740",
    "80",
    "3529",
    "2180",
    "3144013",
    "84585",
    "2324020",
    "39305",
    "1122462",
]


def load_data_to_db(database_name: str, db_params: dict):
    create_database(database_name, db_params)
    employers, vacancies = get_employers_data(EMPLOYER_IDS)

    conn = psycopg2.connect(dbname=database_name, **db_params)
    cur = conn.cursor()

    for emp in employers:
        cur.execute(
            """
            INSERT INTO employers (employer_id, name, url)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """,
            (emp["employer_id"], emp["name"], emp["url"]),
        )

    for vac in vacancies:
        cur.execute(
            """
            INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, currency, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
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
    cur.close()
    conn.close()
