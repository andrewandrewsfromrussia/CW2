import pytest
from src.vacancy import Vacancy  # Замени your_module на имя своего модуля


def test_vacancy_creation_valid():
    vac = Vacancy("123", "Backend Developer", "Москва", 150000, "RUR", "http://example.com/vac")
    assert vac.id == "123"
    assert vac.name == "Backend Developer"
    assert vac.city == "Москва"
    assert vac.salary == 150000
    assert vac.sal_currency == "RUR"
    assert vac.url == "http://example.com/vac"


def test_vacancy_creation_invalid_id():
    with pytest.raises(TypeError):
        Vacancy(123, "Dev", "СПб", 100000, "RUR", "url")


def test_vacancy_creation_invalid_salary_type():
    with pytest.raises(TypeError):
        Vacancy("123", "Dev", "СПб", [100000], "RUR", "url")


def test_get_salary_value_int():
    vac = Vacancy("1", "Dev", "City", 120000, "RUR", "url")
    assert vac._get_salary_value() == 120000


def test_get_salary_value_digit_string():
    vac = Vacancy("1", "Dev", "City", "90000", "RUR", "url")
    assert vac._get_salary_value() == 90000


def test_get_salary_value_range_string():
    vac = Vacancy("1", "Dev", "City", "80000 - 120000", "RUR", "url")
    assert vac._get_salary_value() == 80000


def test_get_salary_value_invalid_string():
    vac = Vacancy("1", "Dev", "City", "дофига", "RUR", "url")
    assert vac._get_salary_value() == 0


def test_lt_operator():
    vac1 = Vacancy("1", "Dev", "City", 100000, "RUR", "url")
    vac2 = Vacancy("2", "Dev", "City", 120000, "RUR", "url")
    assert vac1 < vac2


def test_eq_operator():
    vac1 = Vacancy("1", "Dev", "City", 100000, "RUR", "url")
    vac2 = Vacancy("2", "Dev", "City", 100000, "RUR", "url")
    assert vac1 == vac2


def test_str_method():
    vac = Vacancy("1", "QA", "Новосибирск", "90000 - 100000", "RUR", "url")
    output = str(vac)
    assert "ID: 1" in output
    assert "QA" in output
    assert "90000 - 100000 RUR" in output
