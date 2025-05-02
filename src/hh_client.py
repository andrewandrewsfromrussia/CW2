import requests
from abc import ABC, abstractmethod


class HeadHunterConnect(ABC):
    """
    Абстрактный базовый класс для подключения к API HeadHunter
    """

    @property
    @abstractmethod
    def base_url(self):
        """
        Базовый URL для API
        """
        pass

    @abstractmethod
    def search_vacancies(self, keyword: str, salary: int = None, per_page: int = 20, page: int = 0, area: int = 113, only_with_salary: bool = False):
        """
        Поиск вакансий по ключевому слову
        """
        pass


class HeadHunterAPI(HeadHunterConnect):
    """
    Реализация подключения к HeadHunter API
    """
    # Инициализатор подключения к HeadHunter
    def __init__(self):
        self._base_url = 'https://api.hh.ru/vacancies'

    # Геттер для просмотра URL
    @property
    def base_url(self):
        return self._base_url

    # Метод поиска по вакансии
    def search_vacancies(self, keyword: str, salary: int = None, per_page: int = 20, page: int = 0, area: int = 113, only_with_salary: bool = False):
        params = {
            "text": keyword,                       # Ключевое слово для поиска
            "salary": salary,                      # Зарплата
            "per_page": per_page,                  # Количество вакансий на страницу (0-100)
            "page": page,                          # Номер страницы (по умолчанию 0)
            "area": area,                          # ID города (По умолчанию вся Россия)
            "only_with_salary": only_with_salary   # Опция "только с указанием зарплаты" (по умолчанию False)
        }

        # Обработка подключения
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            vacancies = response.json().get('items', [])
            return vacancies
        else:
            return f"Error: {response.status_code}"
