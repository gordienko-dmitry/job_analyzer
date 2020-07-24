from typing import Union, Tuple, Iterable

from .server import get


VACANCY_URL: str = "https://api.hh.ru/vacancies"


def _get_base_params() -> dict:
    """
    Returns base params for hh vacancy query.
    area: 1 - Moscow
    period: 30 days
    only_with_salary
    and 20 vacancies per page."""

    return {
        "area": 1,
        "period": 30,
        "only_with_salary": True,
        "per_page": 20
    }


def _predict_rub_salary(vacancy) -> Union[int, None]:
    """Solving avg salary of vacancy."""
    salary = vacancy.get("salary")
    if not salary or salary.get("currency") != "RUR":
        return None
    salary_from: Union[int, None] = salary.get("from")
    salary_to: Union[int, None] = salary.get("to")
    if not salary_to and not salary_from:
        return None
    if not salary_to:
        return round(salary_from * 1.2)
    if not salary_from:
        return round(salary_to * 0.8)
    return round((salary_to + salary_from) / 2)


def _get_vacancy_info(text: str, page: int = 1, per_page: int = 20, **kwargs) -> dict:
    """Returns vacancy info from hh api."""
    params: dict = _get_base_params()
    params["text"] = text
    params["page"] = page
    params["per_page"] = per_page
    params.update(kwargs)

    return get(VACANCY_URL, params=params)


def _get_vacancies(query: str) -> Iterable[dict]:
    """Get all vacancies from hh api and returns each vacancy."""
    page_number = 0
    pages_count: int = page_number + 1
    per_page: int = 100
    while pages_count > page_number:
        response_info = _get_vacancy_info(query, page_number, per_page)
        if page_number == 0:
            pages_count = response_info["pages"]
        vacancies = response_info["items"]
        for vacancy in vacancies:
            yield vacancy
        page_number += 1


def _get_avg_salary_and_processed_count(query: str) -> Tuple[int, int]:
    """Solving average salary of hh vacancies."""
    count: int = 0
    sum_salary: int = 0
    for vacancy in _get_vacancies(query):
        avg_salary: Union[int, None] = _predict_rub_salary(vacancy)
        if avg_salary:
            sum_salary += avg_salary
            count += 1
    return int(sum_salary / count) if count else 0, count


def _get_all_vacancies_count(query: str) -> int:
    """Get count vacancies with & without salary."""
    try:
        return _get_vacancy_info(query, page=1, per_page=1, only_with_salary=False)["found"]
    except Exception as ex:
        print(ex)
        return 0


def get_hh_salary_info(queries: list) -> dict:
    """Getting info vacancies & salaries info for query string."""
    salaries_info: dict = {}
    for query in queries:
        salary_info: dict = dict()
        salary_info["vacancies_found"] = _get_all_vacancies_count(query)
        salary_info["average_salary"], salary_info["vacancies_processed"] = \
            _get_avg_salary_and_processed_count(query)
        salaries_info[query] = salary_info

    return salaries_info
