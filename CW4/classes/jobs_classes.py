import requests

from classes.engine_classes import ParsingError, Engine


class HeadHunter(Engine):
    url = 'https://api.hh.ru/vacancies'
    def __init__(self, keyword):
        self.params = {
            "per_page": 100,
            "page": None,
            "text": keyword,
            "archived": False,
        }
        self.headers = {"User-Agent": "Vacancies_ParserApp/1.0"}
        self.vacancies = []


    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f'Ошибка получения вакансий! Статус {response.status_code}')
        return response.json()["items"]


    def get_formatted_vacancies(self):
        formatted_vacancies = []

        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["employer"]["name"],
                "title": vacancy["name"],
                "url": vacancy["alternate_url"],
                "api": "HeadHunter",
            }
            salary = vacancy["salary"]
            if salary:
                formatted_vacancy["salary_from"] = salary['from']
                formatted_vacancy["salary_to"] = salary['to']
                formatted_vacancy["currency"] = salary['currency']
            else:
                formatted_vacancy["salary_from"] = None
                formatted_vacancy["salary_to"] = None
                formatted_vacancy["currency"] = None
            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies


    def get_vacancies(self, pages_count=2):
        self.vacancies = []

        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break


class SuperJob(Engine):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    def __init__(self, keyword):
        self.params = {
            "count": 100,
            "page": None,
            "keyword": keyword,
            "archive": False,
        }
        self.headers = {
            "X-Api-App-Id": 'v3.r.137597605.3c8bcb7d108734e9bd1df52a40e12e86ac71f65f.29a125e2b277709e8ab246b694abfdaec6f9dd10'
        }
        self.vacancies = []


    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f'Ошибка получения вакансий! Статус {response.status_code}')
        return response.json()["objects"]


    def get_formatted_vacancies(self):
        formatted_vacancies = []

        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["firm_name"],
                "title": vacancy["profession"],
                "url": vacancy["link"],
                "api": "SuperJob",
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] and vacancy["payment_from"] != 0 else None,
                "salary_to": vacancy["payment_to"] if vacancy["payment_to"] and vacancy["payment_to"] != 0 else None,
                "currency": vacancy["currency"] if vacancy["currency"] else None
            }
            # if formatted_vacancy["currency"]:
            #     formatted_vacancy["currency"] = vacancy["currency"]
            # else:
            #     formatted_vacancy["currency"] = None
            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies


    def get_vacancies(self, pages_count=2):
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break
