import requests


def get_employers_data(employer_ids):
    """Получает данные о компаниях и их вакансиях."""
    employers = []
    vacancies = []

    for emp_id in employer_ids:
        emp_response = requests.get(f"https://api.hh.ru/employers/{emp_id}")
        if emp_response.status_code != 200:
            continue
        emp_data = emp_response.json()
        employers.append(
            {
                "employer_id": emp_data["id"],
                "name": emp_data["name"],
                "url": emp_data["alternate_url"],
            }
        )

        vac_response = requests.get(
            "https://api.hh.ru/vacancies",
            params={"employer_id": emp_id, "per_page": 100},
        )
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

            vacancies.append(
                {
                    "vacancy_id": item["id"],
                    "employer_id": emp_id,
                    "title": item["name"],
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "currency": currency,
                    "url": item["alternate_url"],
                }
            )

    return employers, vacancies
