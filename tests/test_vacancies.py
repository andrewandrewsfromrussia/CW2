import pytest
from src.vacancies import Vacancies
from src.vacancy import Vacancy


@pytest.fixture
def sample_data():
    return [
        {
            "id": "123",
            "name": "Python Developer",
            "area": {"name": "Москва"},
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "alternate_url": "http://example.com/vac1"
        },
        {
            "id": "456",
            "name": "Data Scientist",
            "area": {"name": "Санкт-Петербург"},
            "salary": {"from": 200000, "currency": "RUR"},
            "alternate_url": "http://example.com/vac2"
        },
        {
            "id": "789",
            "name": "QA Engineer",
            "area": {"name": "Казань"},
            "salary": None,
            "alternate_url": "http://example.com/vac3"
        }
    ]


def test_vacancies_initialization(sample_data):
    vacancies = Vacancies(sample_data)
    assert len(vacancies) == 3

    v1 = vacancies[0]
    assert isinstance(v1, Vacancy)
    assert v1.id == "123"
    assert v1.name == "Python Developer"
    assert v1.city == "Москва"
    assert v1.salary == "100000 - 150000"
    assert v1.sal_currency == "RUR"
    assert v1.url == "http://example.com/vac1"

    v2 = vacancies[1]
    assert v2.salary == 200000
    assert v2.sal_currency == "RUR"

    v3 = vacancies[2]
    assert v3.salary == "Не указано"
    assert v3.sal_currency == ""


def test_vacancies_iteration(sample_data):
    vacancies = Vacancies(sample_data)
    names = [v.name for v in vacancies]
    assert names == ["Python Developer", "Data Scientist", "QA Engineer"]


def test_vacancies_index_access(sample_data):
    vacancies = Vacancies(sample_data)
    assert vacancies[1].name == "Data Scientist"


def test_vacancies_len(sample_data):
    vacancies = Vacancies(sample_data)
    assert len(vacancies) == 3
