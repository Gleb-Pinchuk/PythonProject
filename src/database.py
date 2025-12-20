import psycopg2
from psycopg2 import sql
from typing import Dict, Any


def create_database(database_name: str, params: Dict[str, Any]) -> None:
    """
    Создаёт новую БД, предварительно удалив старую (если существует).
    """
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(database_name))
            )
            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name))
            )
    finally:
        conn.close()

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    employer_id INT PRIMARY KEY,
                    name VARCHAR(255),
                    url VARCHAR(255)
                );
            """)
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id INT PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    title VARCHAR(255),
                    salary_from INT,
                    salary_to INT,
                    currency VARCHAR(10),
                    url VARCHAR(255)
                );
            """)
        conn.commit()
