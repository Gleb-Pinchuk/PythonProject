from abc import ABC, abstractmethod
from typing import List, Optional, Tuple


class VacancyStorage(ABC):
    @abstractmethod
    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        pass

    @abstractmethod
    def get_all_vacancies(
        self,
    ) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        pass

    @abstractmethod
    def get_avg_salary(self) -> float:
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(
        self,
    ) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        pass

    @abstractmethod
    def get_vacancies_with_keyword(
        self, keyword: str
    ) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        pass
