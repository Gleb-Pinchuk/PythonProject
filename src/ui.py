from typing import List, Optional, Tuple
from src.db_manager import DBManager


def _format_salary(s_from: Optional[int], s_to: Optional[int]) -> str:
    if s_from is not None and s_to is not None:
        return f"{s_from} – {s_to}"
    elif s_from is not None:
        return f"от {s_from}"
    elif s_to is not None:
        return f"до {s_to}"
    else:
        return "Не указана"


def show_analysis(db: DBManager) -> None:
    _print_companies_and_vacancies(db)
    _print_all_vacancies(db)
    _print_avg_salary(db)
    _print_higher_salary_vacancies(db)
    _print_python_vacancies(db)


def _print_companies_and_vacancies(db: DBManager) -> None:
    print("\n🏢 Компании и количество вакансий:")
    for company, count in db.get_companies_and_vacancies_count():
        print(f"  • {company}: {count} вакансий")


def _print_all_vacancies(db: DBManager) -> None:
    print("\n📋 Примеры вакансий (первые 5):")
    for row in db.get_all_vacancies()[:5]:
        company, title, s_from, s_to, url = row
        print(f"  • {company} — {title} | Зарплата: {_format_salary(s_from, s_to)} | {url}")


def _print_avg_salary(db: DBManager) -> None:
    avg = db.get_avg_salary()
    print(f"\n💰 Средняя зарплата по вакансиям: {avg:,.0f} ₽".replace(",", " "))


def _print_higher_salary_vacancies(db: DBManager) -> None:
    print("\n📈 Вакансии с зарплатой выше средней:")
    results = db.get_vacancies_with_higher_salary()
    if not results:
        print("  Нет вакансий с зарплатой выше средней.")
        return
    for company, title, s_from, s_to, url in results[:10]:
        print(f"  • {company} — {title} | Зарплата: {_format_salary(s_from, s_to)} | {url}")


def _print_python_vacancies(db: DBManager) -> None:
    keyword = "python"
    print(f"\n🔍 Вакансии с ключевым словом '{keyword}':")
    results = db.get_vacancies_with_keyword(keyword)
    if not results:
        print(f"  Вакансий с '{keyword}' не найдено.")
        return
    for company, title, s_from, s_to, url in results:
        print(f"  • {company} — {title} | Зарплата: {_format_salary(s_from, s_to)} | {url}")
