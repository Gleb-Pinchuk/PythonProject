from src.hh_api import get_employers_data
from src.database import create_database
from src.db_manager import DBManager
import psycopg2

EMPLOYER_IDS = [
    '1455',      # Яндекс
    '1740',      # Сбер
    '80',        # Авито
    '3529',      # Ozon
    '2180',      # VK
    '3144013',   # Тинькофф
    '84585',     # Kaspersky
    '2324020',   # Skyeng
    '39305',     # СберМаркет
    '1122462'    # Газпром нефть
]

DB_PARAMS = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '12345678'
}

DB_NAME = 'hh_vacancies'


def main():
    print("Создание базы данных...")
    create_database(DB_NAME, DB_PARAMS)

    print("Получение данных с hh.ru...")
    employers, vacancies = get_employers_data(EMPLOYER_IDS)

    print("Запись данных в базу...")
    conn = psycopg2.connect(dbname=DB_NAME, **DB_PARAMS)
    cur = conn.cursor()

    for emp in employers:
        cur.execute("""
            INSERT INTO employers (employer_id, name, url)
            VALUES (%s, %s, %s)
            ON CONFLICT (employer_id) DO NOTHING;
        """, (emp['employer_id'], emp['name'], emp['url']))

    for vac in vacancies:
        cur.execute("""
            INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, currency, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING;
        """, (
            vac['vacancy_id'], vac['employer_id'], vac['title'],
            vac['salary_from'], vac['salary_to'], vac['currency'], vac['url']
        ))

    conn.commit()
    cur.close()
    conn.close()

    print("Данные загружены. Работа с DBManager...")

    db = DBManager(DB_NAME, DB_PARAMS)

    print("\nКомпании и количество вакансий:")
    for company, count in db.get_companies_and_vacancies_count():
        print(f"{company}: {count}")

    print("\nСредняя зарплата по RUR:", db.get_avg_salary())

    print("\nВакансии с зарплатой выше средней:")
    for item in db.get_vacancies_with_higher_salary():
        print(f"{item[0]} — {item[1]} | {item[2]}–{item[3]} | {item[4]}")

    print("\nВакансии с ключевым словом 'python':")
    for item in db.get_vacancies_with_keyword('python'):
        print(f"{item[0]} — {item[1]} | {item[2]}–{item[3]} | {item[4]}")


if __name__ == '__main__':
    main()
