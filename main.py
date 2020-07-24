from terminaltables import AsciiTable
from dotenv import load_dotenv
import os

import api

LANGUAGES: list = [
    "Javascript",
    "Java",
    "Python",
    "Ruby",
    "PHP",
    "C++",
    "C#",
    "C",
    "Go",
    "Shell",
    "Objective-C",
    "Scala",
    "Swift",
    "TypeScript"
]


def print_salary_in_table(salary_info: dict, title: str) -> None:
    table_title: list = ["Language", "Vacancies found", "Vacancies processed", "Salary (avg)"]
    title: str = title

    table_data = [table_title]
    for language, hh_info in salary_info.items():
        table_data.append([language, hh_info["vacancies_found"], hh_info["vacancies_processed"],
                           hh_info["average_salary"]])

    # AsciiTable.
    table_instance = AsciiTable(table_data, title)
    print(table_instance.table)
    print()


if __name__ == "__main__":
    load_dotenv()
    sj_key = os.getenv("SUPERJOB_KEY")

    hh_salary_info: dict = api.get_hh_salary_info(LANGUAGES)
    print_salary_in_table(hh_salary_info, "HeadHunter Moscow")

    sj_salary_info: dict = api.get_sj_salary_info(sj_key, LANGUAGES)
    print_salary_in_table(sj_salary_info, "SuperJob Moscow")
