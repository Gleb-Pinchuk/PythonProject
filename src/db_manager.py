from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
from psycopg2 import sql

from src.abc_storage import VacancyStorage


class DBManager(VacancyStorage):
    """Класс для взаимодействия с базой данных PostgreSQL и получения аналитики по вакансиям."""

    def __init__(self, database_name: str, params: Dict[str, Any]) -> None:
        """
        Инициализирует менеджер подключения к БД.

        Args:
            database_name (str): Имя базы данных PostgreSQL.
            params (Dict[str, Any]): Параметры подключения (host, user, password и т.д.).
        """
        self.database_name = database_name
        self.params = params

    @contextmanager
    def _get_connection(self):
        """Контекстный менеджер для безопасного подключения к БД."""
        conn = None
        try:
            conn = psycopg2.connect(dbname=self.database_name, **self.params)
            yield conn
        finally:
            if conn:
                conn.close()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Возвращает список компаний и количество вакансий у каждой."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, COUNT(v.vacancy_id)
                    FROM employers e
                    LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                    GROUP BY e.name;
                """
                )
                return cur.fetchall()

    def get_all_vacancies(
        self,
    ) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """Возвращает все вакансии с информацией о компании, зарплате и ссылке."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.employer_id;
                """
                )
                return cur.fetchall()

    def get_avg_salary(self) -> float:
        """
        Возвращает среднюю зарплату по вакансиям в рублях.
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT AVG(
                        CASE
                            WHEN salary_from IS NOT NULL AND salary_to IS NOT NULL THEN (salary_from + salary_to) / 2.0
                            WHEN salary_from IS NOT NULL THEN salary_from
                            WHEN salary_to IS NOT NULL THEN salary_to
                            ELSE NULL
                        END
                    ) AS avg_salary
                    FROM vacancies
                    WHERE currency = 'RUR' OR currency IS NULL;
                """
                )
                result = cur.fetchone()[0]
                return round(float(result), 2) if result is not None else 0.0

    def get_vacancies_with_higher_salary(
        self,
    ) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """Возвращает вакансии с зарплатой строго выше средней."""
        avg = self.get_avg_salary()
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.employer_id
                    WHERE (
                        CASE
                            WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN (v.salary_from + v.salary_to) / 2.0
                            WHEN v.salary_from IS NOT NULL THEN v.salary_from
                            WHEN v.salary_to IS NOT NULL THEN v.salary_to
                            ELSE 0
                        END
                    ) > %s;
                """,
                    (avg,),
                )
                return cur.fetchall()

    def get_vacancies_with_keyword(
        self, keyword: str
    ) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """
        Возвращает вакансии, в названии которых содержится ключевое слово (регистронезависимо).
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.employer_id
                    WHERE LOWER(v.title) LIKE %s;
                """,
                    (f"%{keyword.lower()}%",),
                )
                return cur.fetchall()
