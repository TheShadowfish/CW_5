import requests
from abc import ABC, abstractmethod
from vacancy import Vacancy

class VacancyConstructor(ABC):
    """
    Абстрактный класс для создания экземпляров класса Vacancy из JSON
    """
    @abstractmethod
    def return_vacancy_list(self, JSON_data: str) -> list[Vacancy]:
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

    def return_vacancy_list(self, JSON_data: str) -> list[Vacancy]:
        """
        {
'id': '94354526',  !!!!ID ВАКАНСИИ, дб оригинальным!!!!
'premium': False,
'name': 'Стажер-разработчик Python',  !!!!ИМЯ ВАКАНСИИ!!!!
'department': None,
'has_test': False,
'response_letter_required': False,
'area': {'id': '76', 'name': 'Ростов-на-Дону', 'url': 'https://api.hh.ru/areas/76'},  !!!!ГЕОГРАФИЯ!!!!
'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR', 'gross': False}, !!!!ЗАРПЛАТА!!!!
'type': {'id': 'open', 'name': 'Открытая'},
'address': None,
'response_url': None,
'sort_point_distance': None,
'published_at': '2024-03-06T16:55:57+0300', !!!!ОПУБЛИКОВАНО!!!!
'created_at': '2024-03-06T16:55:57+0300', !!!!СОЗДАНО!!!!
'archived': False,
'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=94354526',
'show_logo_in_search': None,
'insider_interview': None,
'url': 'https://api.hh.ru/vacancies/94354526?host=hh.ru',
'alternate_url': 'https://hh.ru/vacancy/94354526', !!!!АДРЕС В БРАУЗЕРЕ!!!!
'relations': [],
'employer':
{
'id': '2071925', 'name': 'Додо Пицца', 'url': 'https://api.hh.ru/employers/2071925', 'alternate_url': 'https://hh.ru/employer/2071925',
'logo_urls':{'original': 'https://hhcdn.ru/employer-logo-original/524506.jpg', '240': 'https://hhcdn.ru/employer-logo/2539502.jpeg','90': 'https://hhcdn.ru/employer-logo/2539501.jpeg'},
'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=2071925', 'accredited_it_employer': False, 'trusted': True
},
'snippet': !!!!ОПИСАНИЕ ВАКАНСИИ!!!!
{
'requirement': 'Мы ищем <highlighttext>Python</highlighttext>-разработчика, уровнем от Junior и выше, желательно с опытом развития новых продуктов.
Уверенные знания <highlighttext>Python</highlighttext> 3.8...',
'responsibility': None
},
'contacts': None,
'schedule':{'id': 'fullDay', 'name': 'Полный день'},
'working_days': [],
'working_time_intervals': [],
'working_time_modes': [],
'accept_temporary': False,
'professional_roles': [{'id': '96', 'name': 'Программист, разработчик'}], !!!!professional_roles!!!!
'accept_incomplete_resumes': False,
'experience': {'id': 'noExperience', 'name': 'Нет опыта'}, !!!!ОПЫТ!!!!
'employment': {'id': 'full', 'name': 'Полная занятость'},
'adv_response_url': None, 'is_adv_vacancy': False, 'adv_context': None
}


        :param JSON_data:
        :return:
        """
        pass
