import requests
from abc import ABC, abstractmethod
from src.vacancy import Vacancy


class VacancyConstructor(ABC):
    """
    Абстрактный класс для создания экземпляров класса Vacancy из JSON
    """

    @abstractmethod
    def return_vacancy_list_from_json_list(self, vacancy_json: list[dict]) -> list[Vacancy]:
        pass


class VacancyToFile(ABC):
    """
    Чтение и запись вакансий в файл
    """

    @abstractmethod
    def read_from_file(self, filename: str, **parameters) -> list[Vacancy]:
        pass

    @abstractmethod
    def write_to_file(self, vacancy_list: list[Vacancy]):
        pass


class HhVacancyConstructor(VacancyConstructor):
    """
    Структура JSON с hh

    items = [] - вакансии

    found = 13109
    pages = 100
    page = 0
    per_page = 20
    clusters = None
    arguments = None
    fixes = None
    suggests = None
    alternate_url = https://hh.ru/search/vacancy?enable_snippets=true&text=Python
    """

    def return_vacancy_list_from_json_list(self, vacancy_json: list[dict]) -> list[Vacancy]:
        """
        Парсит полученный JSON - файл и возвращает список (list) объектов Vacancy

        {
        'name': 'Стажер-разработчик Python',  !!!!ИМЯ ВАКАНСИИ!!!!
        'area': {'id': '76', 'name': 'Ростов-на-Дону', 'url': 'https://api.hh.ru/areas/76'},  !!!!ГЕОГРАФИЯ!!!!
        'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR', 'gross': False}, !!!!ЗАРПЛАТА!!!!

        'published_at': '2024-03-06T16:55:57+0300', !!!!ОПУБЛИКОВАНО!!!!
        'created_at': '2024-03-06T16:55:57+0300', !!!!СОЗДАНО!!!!

        'alternate_url': 'https://hh.ru/vacancy/94354526', !!!!АДРЕС В БРАУЗЕРЕ!!!!

        'snippet': !!!!ОПИСАНИЕ ВАКАНСИИ!!!! { 'requirement': 'Мы ищем
        <highlighttext>Python</highlighttext>-разработчика, уровнем от Junior и выше, желательно с опытом развития
        новых продуктов. Уверенные знания <highlighttext>Python</highlighttext> 3.8...', 'responsibility': None },
        'contacts': None, 'schedule':{'id': 'fullDay', 'name': 'Полный день'}, 'professional_roles': [{'id': '96',
        'name': 'Программист, разработчик'}], !!!!professional_roles!!!! 'experience': {'id': 'noExperience',
        'name': 'Нет опыта'}, !!!!ОПЫТ!!!! 'employment': {'id': 'full', 'name': 'Полная занятость'},

        """
        vacancy_list = []

        for elem in vacancy_json:
            name = elem['name']
            url = elem['alternate_url']
            # salary': {'from': 100000, 'to': 150000, 'currency': 'RUR', 'gross': False},
            if elem['salary']:
                salary = elem['salary']['from']
            else:
                salary = None

            region = elem['area']['name']

            pr_roles = ', '.join([role['name'] for role in elem['professional_roles']])

            # requirements = pr_roles + '. ' + str(elem['snippet']['requirement'])
            requirements = ''
            if elem['professional_roles']:
                requirements = f"Специальность: {', '.join([role['name'] for role in elem['professional_roles']])}. "
            if elem['snippet']:
                s = str(elem['snippet']['requirement'])
                s = s.replace('<highlighttext>', '').replace('</highlighttext>', '')
                requirements += s

            v = Vacancy(name, url, salary, region, requirements)
            print(v)
            vacancy_list.append(v)

        return vacancy_list
