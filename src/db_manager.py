import psycopg2
from psycopg2 import sql


class DBManager:
    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params


    def get_companies_and_vacancies_count(self):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()
        cur.execute("""
            SELECT e.name, COUNT(v.vacancy_id)
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name;
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result


    def get_all_vacancies(self):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()
        cur.execute("""
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id;
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result


    def get_avg_salary(self):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()
        cur.execute("""
            SELECT AVG(
                CASE
                    WHEN salary_from IS NOT NULL AND salary_to IS NOT NULL THEN (salary_from + salary_to) / 2
                    WHEN salary_from IS NOT NULL THEN salary_from
                    WHEN salary_to IS NOT NULL THEN salary_to
                    ELSE NULL
                END
            ) AS avg_salary
            FROM vacancies
            WHERE currency = 'RUR' OR currency IS NULL;
        """)
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return round(result, 2) if result else 0


    def get_vacancies_with_higher_salary(self):
        avg = self.get_avg_salary()
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()
        cur.execute("""
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE (
                CASE
                    WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN (v.salary_from + v.salary_to) / 2
                    WHEN v.salary_from IS NOT NULL THEN v.salary_from
                    WHEN v.salary_to IS NOT NULL THEN v.salary_to
                    ELSE 0
                END
            ) > %s;
        """, (avg,))
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result


    def get_vacancies_with_keyword(self, keyword: str):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()
        cur.execute("""
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE LOWER(v.title) LIKE %s;
        """, (f'%{keyword.lower()}%',))
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
