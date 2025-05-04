from src.vacancy import Vacancy


class Vacancies:

    # Инициализатор класса с валидацией некоторых данных и созданием объектов класса Vacancy
    def __init__(self, vacancies_data: list[dict]):
        """Инициализатор класса Vacancies"""
        self.vacancies = []  # Список вакансий класса Vacancy
        for item in vacancies_data:
            id = str(item.get("id", ""))
            name = item.get("name", "Не указано")
            city = item.get("area", {}).get("name", "Не указано")
            salary = item.get("salary")

            if salary:
                sal_currency = salary.get("currency")
                salary_to = salary.get("to")
                salary_from = salary.get("from")
                if salary_from and salary_to:
                    if salary_from == salary_to:
                        salary = salary_from
                    else:
                        salary = f"{salary_from} - {salary.get("to")}"
                elif salary_from:
                    salary = salary_from
                elif salary_to:
                    salary = salary_to
                else:
                    salary = "Не указано"
                    sal_currency = ""
            else:
                salary = "Не указано"
                sal_currency = ""

            url = item.get("alternate_url", "")
            self.vacancies.append(Vacancy(id, name, city, salary, sal_currency, url))

    # Метод итерации для обращения к списку вакансий
    def __iter__(self):
        return iter(self.vacancies)

    # Метод обращения к индексу списка вакансий
    def __getitem__(self, index):
        return self.vacancies[index]

    # Метод обращения к длине списка
    def __len__(self):
        return len(self.vacancies)
