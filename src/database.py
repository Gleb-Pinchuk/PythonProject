import psycopg2
from psycopg2 import sql


def create_database(database_name: str, params: dict):
    """Создаёт базу данных и таблицы."""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(
        sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(database_name))
    )
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE employers (
            employer_id INT PRIMARY KEY,
            name VARCHAR(255),
            url VARCHAR(255)
        );
    """
    )

    cur.execute(
        """
        CREATE TABLE vacancies (
            vacancy_id INT PRIMARY KEY,
            employer_id INT REFERENCES employers(employer_id),
            title VARCHAR(255),
            salary_from INT,
            salary_to INT,
            currency VARCHAR(10),
            url VARCHAR(255)
        );
    """
    )

    conn.commit()
    cur.close()
    conn.close()
