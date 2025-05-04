import os
import json
import pytest
from src.saveJSON import JSONVacancyStorage
from src.vacancy import Vacancy


@pytest.fixture
def sample_vacancies():
    return [
        Vacancy(id="1", name="Python Dev", city="Moscow", salary=150000, sal_currency="RUR",
                url="http://example.com/1"),
        Vacancy(id="2", name="Java Dev", city="SPB", salary=120000, sal_currency="RUR", url="http://example.com/2"),
        Vacancy(id="3", name="Go Dev", city="Moscow", salary=180000, sal_currency="RUR", url="http://example.com/3"),
    ]


def test_file_created_on_init(tmp_path):
    path = tmp_path / "test.json"
    storage = JSONVacancyStorage(filename=path.name)
    assert os.path.exists(storage.filename)


def test_add_vacancy(tmp_path, sample_vacancies):
    storage = JSONVacancyStorage(filename=tmp_path.name + ".json")
    storage._add_vacancy(sample_vacancies[:2])

    with open(storage.filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 2


def test_add_duplicate_vacancy(tmp_path, sample_vacancies):
    storage = JSONVacancyStorage(filename=tmp_path.name + ".json")
    storage._add_vacancy(sample_vacancies[:1])
    storage._add_vacancy(sample_vacancies[:1])
    with open(storage.filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1


def test_get_vacancy_with_filter(tmp_path, sample_vacancies):
    storage = JSONVacancyStorage(filename=tmp_path.name + ".json")
    storage._add_vacancy(sample_vacancies)
    results = storage._get_vacancy(filters={"city": "Moscow"})
    assert all(v.city == "Moscow" for v in results)


def test_top_n(tmp_path, sample_vacancies):
    storage = JSONVacancyStorage(filename=tmp_path.name + ".json")
    storage._add_vacancy(sample_vacancies)
    top = storage.top_n(2)
    assert top[0].salary >= top[1].salary
    assert len(top) == 2


def test_del_vacancy_by_id(tmp_path, sample_vacancies):
    storage = JSONVacancyStorage(filename=tmp_path.name + ".json")
    storage._add_vacancy(sample_vacancies)
    storage._del_vacancy(vacancy_id="2")
    remaining = storage._get_vacancy()
    ids = [v.id for v in remaining]
    assert "2" not in ids
    assert len(remaining) == 2


def test_del_all_vacancies(tmp_path, sample_vacancies):
    storage = JSONVacancyStorage(filename=tmp_path.name + ".json")
    storage._add_vacancy(sample_vacancies)
    storage._del_vacancy(vacancy_id="all")
    remaining = storage._get_vacancy()
    assert len(remaining) == 0


def test_del_duplicates(tmp_path):
    v1 = Vacancy(id="x1", name="Dev", city="Moscow", salary=100000, sal_currency="RUR", url="url")
    v2 = Vacancy(id="x1", name="Dev", city="Moscow", salary=100000, sal_currency="RUR", url="url")
    storage = JSONVacancyStorage(filename=tmp_path.name + ".json")
    storage._add_vacancy([v1, v2])
    storage._del_vacancy(check_unique=True)
    remaining = storage._get_vacancy()
    assert len(remaining) == 1
