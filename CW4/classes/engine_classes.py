from abc import ABC, abstractmethod
import requests


class ParsingError(Exception):
    pass


class Engine(ABC):
    '''Абстрактный класс для работы с API'''

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class Vacancy:
    def __init__(self, vacancy):
        self.employer = vacancy["employer"]
        self.title = vacancy["title"]
        self.url =  vacancy["url"]
        self.api = vacancy["api"]
        self.salary_from = vacancy["salary_from"]
        self.salary_to = vacancy["salary_to"]
        self.currency = vacancy["currency"]
       # self.currency_value = vacancy["currency_value"]


    def __str__(self):

        if not self.salary_from and not self.salary_to:
            salary = "не указано"
        else:
            salary_from, salary_to = '', ''
            if self.salary_from:
                salary_from += f'От {self.salary_from} {self.currency}'
            if self.salary_to:
                salary_to += f'До {self.salary_to} {self.currency}'
            salary = " ".join([salary_from, salary_to]).strip()
        return f'''
        Работадатель: \"{self.employer}\"
        Вакансия: \"{self.title}\"
        Зарплата: \"{salary}\"
        Ссылка: \"{self.url}\"
        '''
