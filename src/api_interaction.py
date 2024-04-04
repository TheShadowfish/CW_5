import requests
from abc import ABC, abstractmethod
from src.vacancy import Vacancy, Employeer


class AbstractApiNoAuth(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями
    """

    @abstractmethod
    def get_vacancies(self, **parameters: dict[str: str]) -> list[dict]:
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class VacancyConstructor(ABC):
    """
    Абстрактный класс для создания экземпляров класса Vacancy из JSON-запроса
    """

    @staticmethod
    @abstractmethod
    def return_vacancy_list_from_json(vacancy_json: list[dict]) -> list[Vacancy]:
        pass


class HhApi(AbstractApiNoAuth, VacancyConstructor):
    """
    Класс для работы с API сервиса hh.ru
    """

    def __init__(self, url: str = 'https://api.hh.ru/vacancies', **parameters: dict[str: str]):
        self.__url = url
        self.__parameters = parameters
        self.found = None
        self.pages = 0
        self.page = 0
        self.per_page = 0

        # print(self.__parameters)
        # input("wait...")

    def get_vacancies(self) -> list[dict]:
        # URL = 'https://api.hh.ru/vacancies'
        # sub_url = 'vacancies'

        res = requests.get(self.__url, params=self.__parameters)
        if res.status_code != 200:
            raise Exception(f"Request code= {res.status_code}, request='{self.__url}', params={self.__parameters}")

        self.found = res.json()['found']
        self.pages = res.json()['pages']
        self.page = res.json()['page']
        self.per_page = res.json()['per_page']

        return res.json()['items']

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self) -> list[dict]:
        # URL = 'https://api.hh.ru/vacancies'

        if self.current < self.pages:
            self.page = self.current
            self.__parameters['page'] = self.page
            self.current += 1
            res = requests.get(self.__url, params=self.__parameters)
            if res.status_code != 200:
                raise Exception(f"Request code= {res.status_code}, request='{self.__url}', params={self.__parameters}")
            return res.json()['items']
        else:
            raise StopIteration

    def __repr__(self):
        repr_list = [str(i[0]) + ': ' + str(i[1]) for i in self.__dict__.items()]
        return f"<{self.__class__.__name__}({', '.join(repr_list)})>"

    def __str__(self):
        repr_list = [str(i[0]) + ': ' + str(i[1]) for i in self.__dict__.items()]
        delimiter = '\n\t'
        return f"{self.__class__.__name__}{delimiter}{delimiter.join(repr_list)}"

    @classmethod
    def get_area_id(cls, area_name: str = 'Москва') -> str | None:
        """
        Возврат ID по имени населенного пункта или области
        """
        url_area = 'https://api.hh.ru/areas'
        res = requests.get(url_area)

        if res.status_code != 200:
            raise Exception(f"Request code= {res.status_code}, request='{url_area}'")

        area = res.json()
        result = cls.__recursive_find_area_id(area, area_name)

        return result

    @classmethod
    def __recursive_find_area_id(cls, areas, area_name) -> int | None:
        """
        Найти в древовидной структуре словаря areas (HH.ru) искомый город
        """
        for area in areas:
            if area['name'] == area_name:
                return area['id']
            elif isinstance(area['areas'], list) and len(area['areas']) > 0:
                result = cls.__recursive_find_area_id(area['areas'], area_name)
                if result is not None:
                    return result
            else:
                continue
        else:
            return None

    @classmethod
    def get_professional_roles(cls) -> list[dict]:
        """
        Возвращает справочник профессий
        """
        url_professional_roles = 'https://api.hh.ru/professional_roles'
        res = requests.get(url_professional_roles)

        if res.status_code != 200:
            raise Exception(f"Request code= {res.status_code}, request='{url_professional_roles}'")

        area = res.json()
        result = area

        return result

    @classmethod
    def get_professional_roles_id(cls, role_name: str = 'Информационные технологии') -> int | None:
        """
        Возвращает справочник профессий
        """
        url_professional_roles = 'https://api.hh.ru/professional_roles'
        res = requests.get(url_professional_roles)

        if res.status_code != 200:
            raise Exception(f"Request code= {res.status_code}, request='{url_professional_roles}'")

        professional_roles = res.json()
        result = cls.__find_professional_role_id(professional_roles, role_name)
        return result

    @classmethod
    def __find_professional_role_id(cls, professional_roles, role_name) -> int | list[int] | None:
        """
        Найти id по названию профессии
        """
        role_name = role_name.lower()

        for role in professional_roles['categories']:
            if role_name in role['name'].lower().split(', '):
                roles_list = []
                for sub_role in role['roles']:
                    roles_list.append(sub_role['id'])
                return roles_list
            elif isinstance(role['roles'], list) and len(role['roles']) > 0:
                for sub_role in role['roles']:
                    if role_name.lower() in sub_role['name'].lower().split(', '):
                        return sub_role['id']
            else:
                continue
        else:
            return None

    @staticmethod
    def return_vacancy_list_from_json(vacancy_json: list[dict]) -> list[Vacancy]:

        """
        Парсит полученный JSON - файл и возвращает список (list) объектов Vacancy

        Некоторые ключи в получаемом JSON
        {
        'name': 'Стажер-разработчик Python',  !!!!ИМЯ ВАКАНСИИ!!!!
        'area': {'id': '76', 'name': 'Ростов-на-Дону', 'url': 'https://api.hh.ru/areas/76'},  !!!!ГЕОГРАФИЯ!!!!
        'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR', 'gross': False}, !!!!ЗАРПЛАТА!!!!

        'published_at': '2024-03-06T16:55:57+0300', !!!!ОПУБЛИКОВАНО!!!!
        'created_at': '2024-03-06T16:55:57+0300', !!!!СОЗДАНО!!!!

        'alternate_url': 'https://hh.ru/vacancy/94354526', !!!!АДРЕС В БРАУЗЕРЕ!!!!

        'snippet': !!!!ОПИСАНИЕ ВАКАНСИИ!!!!
        {
        'requirement': 'Мы ищем <highlighttext>Python</highlighttext>-разработчика, уровнем от Junior и выше,
        желательно с опытом развития новых продуктов. Уверенные знания <highlighttext>Python</highlighttext> 3.8...',
        'responsibility': None
        },
        'contacts': None,
        'schedule':{'id': 'fullDay', 'name': 'Полный день'},
        'professional_roles': [{'id': '96', 'name': 'Программист, разработчик'}], !!!!professional_roles!!!!
        'experience': {'id': 'noExperience', 'name': 'Нет опыта'}, !!!!ОПЫТ!!!!
        'employment': {'id': 'full', 'name': 'Полная занятость'},

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

            requirements = ''
            if elem['professional_roles']:
                requirements = f"Специальность: {', '.join([role['name'] for role in elem['professional_roles']])}. "
            if elem['snippet']:
                s = str(elem['snippet']['requirement'])
                s = s.replace('<highlighttext>', '').replace('</highlighttext>', '')
                requirements += s

            employeer_id = elem['employer']['id']

            v = Vacancy(name, url, salary, region, requirements, employeer_id)
            vacancy_list.append(v)

        return vacancy_list

    def return_employer_list_from_json(vacancy_json: list[dict]) -> list[Employeer]:

        """
        Парсит полученный JSON - файл и возвращает список (list) объектов Vacancy

        Некоторые ключи в получаемом JSON
        {
        ...
        'employer':
            {
            'id': '1795976',
            'name': 'Университет ИТМО',
            'url': 'https://api.hh.ru/employers/1795976',
            'alternate_url': 'https://hh.ru/employer/1795976',
            'logo_urls':
                {
                'original': 'https://img.hhcdn.ru/employer-logo-original/1008510.jpg',
                '90': 'https://img.hhcdn.ru/employer-logo/5654816.jpeg',
                '240': 'https://img.hhcdn.ru/employer-logo/5654817.jpeg'
                },
            'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=1795976',
            'accredited_it_employer': False,
            'trusted': True
            },
        ...
        }

        """
        emplorer_list = []

        for i, elem in enumerate(vacancy_json, start =1):
            # print("start_elem\n")
            # print(f"Employeer {i}) {elem['employer']}")
            # input("\nend_elem")

            employeer_id = elem['employer']['id']
            name = elem['employer']['name']
            url = elem['employer']['alternate_url']
            vacancies_url = elem['employer']['vacancies_url']

            # salary': {'from': 100000, 'to': 150000, 'currency': 'RUR', 'gross': False},

            requirements = ''
            if elem['professional_roles']:
                requirements = f"Специальность: {', '.join([role['name'] for role in elem['professional_roles']])}. "
            if elem['snippet']:
                s = str(elem['snippet']['requirement'])
                s = s.replace('<highlighttext>', '').replace('</highlighttext>', '')
                requirements += s

            v = Employeer(employeer_id, name, url, vacancies_url)
            emplorer_list.append(v)

        return emplorer_list

    @classmethod
    def check_parameters_to_request(cls, parameters: dict) -> dict:
        """
        Проверка параметров для последующей передачи в запрос к Api

        Ключи словаря parameters после user_input:

        platforms = parameters['platforms']
        professional_role = parameters['professional_role']
        filter_region = parameters['filter_region']
        top_n = parameters['top_n']
        filter_words = parameters['filter_words']
        salary_range = parameters['salary_range']
        """

        # найти идентификатор региона и профессии
        # без этого получаемые данные плохо подходят для сортировки
        print(f"Get region_id and profession_id from hh.ru... "
              f"({parameters['filter_region']}, {parameters['professional_role']})")

        region_id = cls.get_area_id(parameters['filter_region'])
        profession_id = cls.get_professional_roles_id(parameters['professional_role'])

        print("Done!")

        # параметры запроса
        parameters['area'] = region_id
        parameters['professional_role'] = profession_id
        parameters['text'] = ' AND '.join(parameters['filter_words'])

        if parameters['salary_range'] != '':
            salary = [int(s.strip()) for s in parameters['salary_range'].split('-') if s.strip().isdigit()]
            parameters['salary'] = sum(salary) // 2
            parameters['only_with_salary'] = True

        return parameters
