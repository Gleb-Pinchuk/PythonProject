import requests
from typing import List, Dict, Any, Tuple


def get_employers_data(employer_ids: List[str]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Получает данные о компаниях и их открытых вакансиях через API hh.ru.
    """
    employers = []
    vacancies = []

    for emp_id in employer_ids:
        # Получение данных о работодателе
        emp_url = f"https://api.hh.ru/employers/{emp_id}"
        try:
            emp_response = requests.get(emp_url, timeout=10)
        except requests.RequestException:
            continue

        if emp_response.status_code != 200:
            continue

        emp_data = emp_response.json()
        employers.append({
            "employer_id": emp_data["id"],
            "name": emp_data["name"],
            "url": emp_data.get("alternate_url", ""),
        })

        vac_url = "https://api.hh.ru/vacancies"
        try:
            vac_response = requests.get(
                vac_url,
                params={"employer_id": emp_id, "per_page": 100},
                timeout=10
            )
        except requests.RequestException:
            continue

        if vac_response.status_code != 200:
            continue

        vac_data = vac_response.json()
        for item in vac_data.get("items", []):
            salary = item.get("salary")
            if salary:
                salary_from = salary.get("from")
                salary_to = salary.get("to")
                currency = salary.get("currency")
            else:
                salary_from = salary_to = currency = None

            vacancies.append({
                "vacancy_id": item["id"],
                "employer_id": emp_id,
                "title": item["name"],
                "salary_from": salary_from,
                "salary_to": salary_to,
                "currency": currency,
                "url": item.get("alternate_url", ""),
            })

    return employers, vacancies
