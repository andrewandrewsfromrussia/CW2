import pytest
from unittest.mock import patch
from src.hh_client import HeadHunterAPI

# Тест успешного запроса
@patch("src.hh_client.requests.get")
def test_search_vacancies_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"id": "1", "name": "Python Developer"}]}

    hh_api = HeadHunterAPI()
    result = hh_api.search_vacancies("Python")

    assert isinstance(result, list)
    assert result[0]["id"] == "1"
    assert result[0]["name"] == "Python Developer"

# Тест запроса с ошибкой (например, 403 Forbidden)
@patch("src.hh_client.requests.get")
def test_search_vacancies_error(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 403
    hh_api = HeadHunterAPI()
    result = hh_api.search_vacancies("Python")

    assert isinstance(result, str)
    assert result.startswith("Error:")
    assert "403" in result

# Тест параметров запроса (важно, что параметры правильно передаются)
@patch("src.hh_client.requests.get")
def test_search_vacancies_params(mock_get):
    hh_api = HeadHunterAPI()
    hh_api.search_vacancies("Python", salary=100000, per_page=50, page=1, area=1, only_with_salary=True)

    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert kwargs["params"]["text"] == "Python"
    assert kwargs["params"]["salary"] == 100000
    assert kwargs["params"]["per_page"] == 50
    assert kwargs["params"]["page"] == 1
    assert kwargs["params"]["area"] == 1
    assert kwargs["params"]["only_with_salary"] is True
