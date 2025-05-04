import os
import json
from abc import abstractmethod, ABC
from src.vacancy import Vacancy


class VacancyStorage(ABC):
    """Абстрактный класс обязательств реализации методов сохранения"""
    @abstractmethod
    def _add_vacancy(self, vacancy: dict) -> None:
        """Добавляет вакансию в файл"""
        pass

    @abstractmethod
    def _get_vacancy(self, **criteria) -> list[dict]:
        """Получает вакансии по критериям"""
        pass

    @abstractmethod
    def _del_vacancy(self, vacancy_id: str) -> None:
        """Удаляет вакансию по id или другому признаку"""
        pass


class JSONVacancyStorage(VacancyStorage):
    """Класс для работы с вакансиями в JSON"""

    def __init__(self, filename: str = "vacancies.json"):
        """Метод инициализации файла с сохранением"""
        self.filename = os.path.join("..", "data", filename)
        self.__ensure_file_exist()

    def __ensure_file_exist(self):
        directory = os.path.dirname(self.filename)

        # Проверка на наличие директории
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Проверка на наличие файла
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _add_vacancy(self, vacancies: list[Vacancy]):
        """Метод сохранения данных в файл, добавляет новые вакансии в конец файла"""
        # Проверка на существование и пустоту файла
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            existing = []
        else:
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except (json.JSONDecodeError, IOError):
                existing = []

        # Получаем все ID существующих вакансий
        existing_ids = {vacancy["id"] for vacancy in existing}

        # Преобразуем объекты Vacancy в словари и проверяем уникальность ID
        new_data = [
            {
                "id": v.id,
                "name": v.name,
                "city": v.city,
                "salary": v.salary,
                "sal_currency": v.sal_currency,
                "url": v.url
            }
            for v in vacancies if v.id not in existing_ids  # Добавляем только уникальные вакансии
        ]

        # Если есть новые вакансии, добавляем их в список и сохраняем
        if new_data:
            existing.extend(new_data)
            # Сохранение обновленных данных в файл
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(existing, f, ensure_ascii=False, indent=2)
            print(f"Добавлено {len(new_data)} вакансий")
        else:
            print("Нет новых вакансий для добавления")

    def _get_vacancy(self, count=5, filters: dict = None) -> list[Vacancy]:
        """Метод получения списка объектов Vacancy из файла"""
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

        if not isinstance(data, list) or len(data) == 0:
            return []

        # Фильтрация
        if filters:
            for key, value in filters.items():
                data = [d for d in data if str(d.get(key, "")).lower() == str(value).lower()]

        # Ограничение по количеству
        data = data[:count]

        vacancies = []
        for item in data:
            try:
                vacancy = Vacancy(
                    id=item["id"],
                    name=item["name"],
                    city=item["city"],
                    salary=item["salary"],
                    sal_currency=item["sal_currency"],
                    url=item["url"]
                )
                vacancies.append(vacancy)
            except Exception as e:
                print(f"[Ошибка при создании Vacancy]: {e}")
                continue

        return vacancies

    def get_vacancy(self, count: int = 1000, filters: dict = None):
        """Публичный метод для получения вакансий из файла"""
        vacancies = self._get_vacancy(count=count, filters=filters)

        if not vacancies:
            print("Файл с вакансиями пуст")
            return

        for vacancy in vacancies:
            print(vacancy)

        print("Конец списка вакансий")  # Убери эту строку, если не хочешь видеть финальный вывод

    def top_n(self, n: int):
        """Метод для получения топ N вакансий по зарплате."""
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Список для вакансий
        vacancies = []

        for item in data:
            salary = item.get("salary")

            # Проверяем тип зарплаты
            if isinstance(salary, int):
                item["salary"] = salary
            elif isinstance(salary, str):
                if " - " in salary:
                    try:
                        min_salary = salary.split(" - ")[0]
                        item["salary"] = int(min_salary.replace(",", "").replace(" ", ""))
                    except ValueError:
                        item["salary"] = 0
                else:
                    try:
                        item["salary"] = int(salary.replace(",", "").replace(" ", ""))
                    except ValueError:
                        item["salary"] = 0

            vacancy = Vacancy(
                id=item["id"],
                name=item["name"],
                city=item["city"],
                salary=item["salary"],
                sal_currency=item["sal_currency"],
                url=item["url"]
            )
            vacancies.append(vacancy)

        # Сортировка по зарплате (по убыванию)
        sorted_vacancies = sorted(vacancies, key=lambda v: v.salary, reverse=True)

        # Возвращает топ N
        top_n_vacancies = sorted_vacancies[:n]

        # Выводти вакансии
        for vacancy in top_n_vacancies:
            print(vacancy)

        return top_n_vacancies

    def _del_vacancy(self, vacancy_id: str = "", check_unique: bool = False):
        """Метод удаления вакансии по ID с возможностью удаления всех данных
           и опцией проверки на уникальность (удаляет дубликаты)"""

        # Загружаем данные из файла
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Преобразует данные в объект Vacancy
        vacancies = [Vacancy(**item) for item in data]

        # Если указан "all", удаляет все вакансии
        if vacancy_id == "all":
            vacancies.clear()
        else:
            vacancies = [vacancy for vacancy in vacancies if vacancy.id != vacancy_id]

        # Проверка всех ID на уникальные значения
        if check_unique:
            seen_ids = set()
            vacancies = [vacancy for vacancy in vacancies if
                         vacancy.id not in seen_ids and not seen_ids.add(vacancy.id)]

        new_data = [
            {
                "id": v.id,
                "name": v.name,
                "city": v.city,
                "salary": v.salary,
                "sal_currency": v.sal_currency,
                "url": v.url
            }
            for v in vacancies
        ]

        # Сохранение обновленных данных в файл
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)

        # Сообщение о результатах
        if vacancy_id == "all":
            print("Все вакансии были удалены.")
        elif len(vacancies) < len(data):
            print(f"Вакансия с ID {vacancy_id} была удалена.")
        else:
            print(f"Вакансия с ID {vacancy_id} не найдена.")
