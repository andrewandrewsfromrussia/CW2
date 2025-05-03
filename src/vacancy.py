

class Vacancy:
    __slots__ = ("id", "name", "city", "salary", "sal_currency", "url")

    def __init__(self, id: str, name: str, city: str, salary: int, sal_currency: str, url: str):
        self.id = id
        self.name = name
        self.city = city
        self.salary = salary
        self.sal_currency = sal_currency
        self.url = url
        self._validate_fields()

    def _validate_fields(self):
        if not isinstance(self.id, str):
            raise TypeError("Некорректное ID")
        if not isinstance(self.name, str):
            raise TypeError("Некорректное имя вакансии")
        if not isinstance(self.city, str):
            raise TypeError("Некорректное имя города")
        if not (isinstance(self.salary, int) or isinstance(self.salary, str)):
            raise TypeError("Зарплата должна быть числом или строкой")
        if not isinstance(self.sal_currency, str):
            raise TypeError("Некорректная валюта")
        if not isinstance(self.url, str):
            raise TypeError("Некорректный URL")

    def __str__(self):
        return (f"ID: {self.id}\n{self.name}\nГород: {self.city} "
                f"| Зарплата: {self.salary} {self.sal_currency}\n{self.url}\n")

    def _get_salary_value(self):
        """Метод для взаимодействия с диапазоном зарплат"""
        if isinstance(self.salary, int):
            return self.salary
        if isinstance(self.salary, str):
            if self.salary.isdigit():
                return int(self.salary)
            elif "-" in self.salary:
                parts = self.salary.split("-")
                try:
                    return int(parts[0].strip())
                except ValueError:
                    return 0
        return 0

    def __lt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._get_salary_value() < other._get_salary_value()

    def __eq__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._get_salary_value() == other._get_salary_value()
