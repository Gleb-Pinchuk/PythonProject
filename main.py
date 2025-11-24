"""
Точка входа в приложение.

Загружает данные о вакансиях с hh.ru в PostgreSQL и выводит аналитику:
- список компаний и количество вакансий,
- среднюю зарплату,
- вакансии с зарплатой выше средней,
- вакансии по ключевому слову (например, 'python').
"""

from typing import List, Optional, Tuple

from src.app import load_data_to_db
from src.config import load_db_config
from src.db_manager import DBManager

DB_NAME = "hh_vacancies"


def print_companies_and_vacancies(db: DBManager) -> None:
    """Выводит список компаний и количество вакансий."""
    print("\n🏢 Компании и количество вакансий:")
    results: List[Tuple[str, int]] = db.get_companies_and_vacancies_count()
    for company, count in results:
        print(f"  • {company}: {count} вакансий")


def print_all_vacancies(db: DBManager) -> None:
    """Выводит все вакансии (ограничено первыми 5 для краткости)."""
    print("\n📋 Примеры вакансий (первые 5):")
    results: List[Tuple[str, str, Optional[int], Optional[int], str]] = (
        db.get_all_vacancies()
    )
    for company, title, s_from, s_to, url in results[:5]:
        salary = f"{s_from or '—'} – {s_to or '—'}" if s_from or s_to else "Не указана"
        print(f"  • {company} — {title} | Зарплата: {salary} | {url}")


def print_avg_salary(db: DBManager) -> None:
    """Выводит среднюю зарплату."""
    avg: float = db.get_avg_salary()
    print(f"\n💰 Средняя зарплата по вакансиям: {avg:,.0f} ₽".replace(",", " "))


def print_higher_salary_vacancies(db: DBManager) -> None:
    """Выводит вакансии с зарплатой выше средней."""
    print("\n📈 Вакансии с зарплатой выше средней:")
    results: List[Tuple[str, str, Optional[int], Optional[int], str]] = (
        db.get_vacancies_with_higher_salary()
    )
    if not results:
        print("  Нет вакансий с зарплатой выше средней.")
        return
    for company, title, s_from, s_to, url in results[:10]:  # ограничим для читаемости
        salary = f"{s_from or '—'} – {s_to or '—'}" if s_from or s_to else "Не указана"
        print(f"  • {company} — {title} | Зарплата: {salary} | {url}")


def print_python_vacancies(db: DBManager) -> None:
    """Выводит вакансии с ключевым словом 'python'."""
    keyword = "python"
    print(f"\n🔍 Вакансии с ключевым словом '{keyword}':")
    results: List[Tuple[str, str, Optional[int], Optional[int], str]] = (
        db.get_vacancies_with_keyword(keyword)
    )
    if not results:
        print(f"  Вакансий с '{keyword}' не найдено.")
        return
    for company, title, s_from, s_to, url in results:
        salary = f"{s_from or '—'} – {s_to or '—'}" if s_from or s_to else "Не указана"
        print(f"  • {company} — {title} | Зарплата: {salary} | {url}")


def main() -> None:
    """Основная функция запуска приложения."""
    try:
        config = load_db_config()
        print("🔄 Загрузка данных из hh.ru и сохранение в PostgreSQL...")
        load_data_to_db(DB_NAME, config)

        print("✅ Данные успешно загружены. Анализ:")
        db = DBManager(DB_NAME, config)

        print_companies_and_vacancies(db)
        print_all_vacancies(db)
        print_avg_salary(db)
        print_higher_salary_vacancies(db)
        print_python_vacancies(db)

    except Exception as e:
        print(f"\n❌ Ошибка при выполнении: {e}")
        raise


if __name__ == "__main__":
    main()
