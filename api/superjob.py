from typing import Union, Tuple, Iterable, Optional

from .server import get
from .salary import predict_rub_salary


VACANCY_URL: str = "https://api.superjob.ru/2.0/vacancies/"


def _get_base_params() -> dict:
    """
    Returns base params for sj vacancy query.
    town: 4 - Moscow
    catalogues: 48 - Development, programming
    "period": 30 days."""

    return {
        "town": 4,
        "catalogues": 48,
        "period": 30
    }


def _get_base_headers(key: str) -> dict:
    """
    Returns base headers for sj vacancy query.
    It's one secret key header."""

    return {"X-Api-App-Id": key}


def _predict_rub_salary(vacancy) -> Union[int, None]:
    """Solving avg salary of vacancy."""
    currency: str = vacancy.get("currency", "")
    if not currency or currency != "rub":
        return None
    salary_from: Union[int, None] = vacancy.get("payment_from")
    salary_to: Union[int, None] = vacancy.get("payment_to")
    return predict_rub_salary(salary_from, salary_to, currency)


def _get_vacancy_info(key: str, text: str, page: int = 1, count: int = 20, **kwargs) -> dict:
    """Returns vacancy info from sj api."""
    params: dict = _get_base_params()
    params["keyword"] = text
    params["page"] = page
    params["count"] = count
    params.update(kwargs)

    headers: dict = _get_base_headers(key)

    return get(VACANCY_URL, params=params, headers=headers)


def _get_vacancies(key, query: str) -> Iterable[dict]:
    """Get all vacancies from sj api and returns each vacancy."""
    page_number = 0
    pages_count: int = page_number + 1
    count: int = 100
    while pages_count > page_number:
        response_info = _get_vacancy_info(key, query, page_number, count)
        if page_number == 0:
            pages_count = response_info["total"] // count + 1
        vacancies = response_info["objects"]
        for vacancy in vacancies:
            yield vacancy
        page_number += 1


def _get_avg_salary_and_processed_count(key: str, query: str) -> Tuple[int, int]:
    """Solving average salary of sj vacancies."""
    count: int = 0
    sum_salary: int = 0
    for vacancy in _get_vacancies(key, query):
        avg_salary: Union[int, None] = _predict_rub_salary(vacancy)
        if avg_salary:
            sum_salary += avg_salary
            count += 1
    return int(sum_salary / count) if count else 0, count


def _get_all_vacancies_count(key: str, query: str) -> Optional[int]:
    """Get count vacancies."""
    try:
        return _get_vacancy_info(key, query, page=1, count=1)["total"]
    except Exception as ex:
        print(ex)
        return


def get_sj_salary_info(key: str, queries: list) -> dict:
    """Getting info vacancies & salaries info for query string."""
    salaries_info: dict = {}
    for query in queries:
        salary_info: dict = dict()
        salary_info["vacancies_found"] = _get_all_vacancies_count(key, query)
        salary_info["average_salary"], salary_info["vacancies_processed"] = \
            _get_avg_salary_and_processed_count(key, query)
        salaries_info[query] = salary_info

    return salaries_info
