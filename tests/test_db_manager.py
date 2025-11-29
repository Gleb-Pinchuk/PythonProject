import psycopg2
import pytest

from src.database import create_database
from src.db_manager import DBManager

DB_PARAMS = {
    "host": "localhost",
    "user": "postgres",
    "password": "12345678"
}
TEST_DB_NAME = "test_hh_db_pytest"


@pytest.fixture(scope="session")
def db_manager():
    """Создаёт тестовую БД, наполняет данными и возвращает DBManager."""
    # Создаём БД
    create_database(TEST_DB_NAME, DB_PARAMS)

    with psycopg2.connect(dbname=TEST_DB_NAME, **DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO employers (employer_id, name, url) VALUES (%s, %s, %s)",
                (1, "Альфа-Банк", "https://hh.ru/employer/1"),
            )
            cur.execute(
                "INSERT INTO employers (employer_id, name, url) VALUES (%s, %s, %s)",
                (2, "Сбер", "https://hh.ru/employer/2"),
            )

            cur.execute("""
                INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, currency, url)
                VALUES
                (101, 1, 'Python Developer', 100000, 150000, 'RUR', 'https://hh.ru/vacancy/101'),
                (102, 1, 'Junior Python Dev', 70000, NULL, 'RUR', 'https://hh.ru/vacancy/102'),
                (103, 2, 'Data Analyst', NULL, 120000, 'RUR', 'https://hh.ru/vacancy/103'),
                (104, 2, 'Java Developer', 90000, 130000, 'RUR', 'https://hh.ru/vacancy/104'),
                (105, 2, 'Python ML Engineer', 140000, 200000, 'RUR', 'https://hh.ru/vacancy/105')
            """)

    yield DBManager(TEST_DB_NAME, DB_PARAMS)

    with psycopg2.connect(dbname="postgres", **DB_PARAMS) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")


def test_get_companies_and_vacancies_count(db_manager):
    result = db_manager.get_companies_and_vacancies_count()
    assert len(result) == 2
    result_dict = {name: count for name, count in result}
    assert result_dict["Альфа-Банк"] == 2
    assert result_dict["Сбер"] == 3


def test_get_all_vacancies(db_manager):
    result = db_manager.get_all_vacancies()
    assert len(result) == 5
    assert result[0][0] == "Альфа-Банк"
    assert "Python" in result[0][1]


def test_get_avg_salary(db_manager):
    avg = db_manager.get_avg_salary()
    # (100+150)/2 = 125, 70, 120, (90+130)/2 = 110, (140+200)/2 = 170
    # Среднее = (125 + 70 + 120 + 110 + 170) / 5 = 595 / 5 = 119.0
    assert abs(avg - 119000.0) < 0.01


def test_get_vacancies_with_higher_salary(db_manager):
    result = db_manager.get_vacancies_with_higher_salary()
    avg = db_manager.get_avg_salary()  # ≈119000

    for row in result:
        s_from, s_to = row[2], row[3]
        if s_from is not None and s_to is not None:
            salary = (s_from + s_to) / 2
        else:
            salary = s_from or s_to or 0
        assert salary > avg

    titles = {row[1] for row in result}
    assert "Python ML Engineer" in titles
    assert "Python Developer" in titles
    assert "Data Analyst" in titles
    assert "Junior Python Dev" not in titles
    assert "Java Developer" not in titles


def test_get_vacancies_with_keyword(db_manager):
    result = db_manager.get_vacancies_with_keyword("Python")
    assert len(result) == 3
    for row in result:
        assert "python" in row[1].lower()
