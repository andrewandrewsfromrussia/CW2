from src.hh_client import HeadHunterAPI
from src.vacancy import Vacancy
from src.vacancies import Vacancies
from src.saveJSON import JSONVacancyStorage


def user_interaction():
    """Функция имитации пользовательского интерфейса"""
    print("Доброго времени суток!")

    saver = JSONVacancyStorage()  # Название файла для сохранения файла внутри скобок (если нужно)
    api = HeadHunterAPI()

    while True:
        print("\nВыберите действие:")
        print("\n1. Поиск вакансий")
        print("2. Показать существующие вакансии")
        print("3. Показать Топ N вакансий по зарплате")
        print("4. Очистить файл")
        print("5. Выход")

        choise = input("\nПользователь: ").strip()

        if choise == "1":
            keyword = input("Введите поисковой запрос: ")
            salary = int(input("Введите желаемую зарплату: "))
            per_page = int(input("Введите количество вакансий (максимум 100): "))
            vacancies_json = api.search_vacancies(
                keyword=keyword,
                salary=salary,
                per_page=per_page
            )
            vacancies = Vacancies(vacancies_json)
            print(f"Найдено вакансий: {len(vacancies)}")
            choise_one = input("Хотите сохранить? y/n [y]\nПользователь: ")
            if choise_one =="y":
                saver._add_vacancy(vacancies)
            elif choise_one == "n":
                continue
        elif choise == "2":
            file_vacancies = saver.get_vacancy()
            file_vacancies
            print("1. Сортировать вакансии по зарплате")
            print("2. Удалить вакансию по id")
            print("3. Главное меню")
            choise_two = input("Выберите действие\nПользователь: ")
            if choise_two == "1":
                sorted_file = saver.top_n(10000)
                sorted_file
            elif choise_two == "2":
                del_vacancy = saver._del_vacancy(input("Введите id вакансии: "))
                del_vacancy
            elif choise_two == "3":
                continue
        elif choise == "3":
            top_n = int(input("Введите ожидаемое N топа: "))
            top_vacancy = saver.top_n(top_n)
            top_vacancy
        elif choise == "4":
            saver._del_vacancy("all")
        elif choise == "5":
            break
