import json

from classes.engine_classes import Vacancy


class Connector:
    def __init__(self, keyword, vacancies_json):
        self.filename = f"{keyword.title()}.json"
        self.insert(vacancies_json)

    def insert(self, vacancies_json):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(vacancies_json, file, indent=4)

    def select(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        return [Vacancy(x) for x in vacancies]

    def sort_by_salary_from(self):
        desc = True if input(
            "> - DESC \n"
            "< - ASC \n>>>"
        ).lower() == ">" else False
        vacancies = self.select()
        return sorted(vacancies, key=lambda x: (x.salary_from if x.salary_from else 0, x.salary_to if x.salary_to else 0), reverse=desc)
