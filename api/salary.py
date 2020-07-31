from typing import Union


def predict_rub_salary(salary_from: Union[int, None], salary_to: Union[int, None], currency: str) -> Union[int, None]:
    """Solving avg salary of vacancy."""
    if currency != "RUR":
        return None
    if not salary_to and not salary_from:
        return None
    if not salary_to:
        return round(salary_from * 1.2)
    if not salary_from:
        return round(salary_to * 0.8)
    return round((salary_to + salary_from) / 2)
