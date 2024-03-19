import pytest

from src.vacancy import Vacancy


@pytest.fixture
def empty_vacancy():
    return Vacancy(None, None, None, None, None)


@pytest.fixture
def salary_real_vacancy():
    return Vacancy('Разработчик в зоопарк.', 'https://moscowzoo.ru/', '100500999', 'Москва',
                   "Необходимо умение GNUть антилоп и гладить манула (не кусь!). Опыт по взаимодействию с python'ом "
                   "обязателен.")


@pytest.fixture
def second_real_vacancy():
    return Vacancy('Разработчик Python.', 'ссылка на сайт', '100500', 'Санкт-Петербург',
                   "Много разного")


@pytest.fixture
def first_real_vacancy():
    return Vacancy('Разработчик Python.', 'ссылка на сайт', '100500', 'Санкт-Петербург',
                   "Много разного")


@pytest.fixture
def serialized_second_real_vacancy():
    return {'_Vacancy__name': 'Разработчик Python.', '_Vacancy__url': 'ссылка на сайт', '_Vacancy__salary': 100500,
            '_Vacancy__region': 'Санкт-Петербург', '_Vacancy__requirements': "Много разного"}


@pytest.fixture
def test_filters():
    vacancy_list = [
        Vacancy('Разработчик Python.', 'url', '0', 'Санкт-Петербург', "Программист, разработчик"),
        Vacancy('Разработчик Python.', 'url', '40000', 'Санкт-Петербург', "fullstack"),
        Vacancy('Инженер.', 'url', '50000', 'Архангельск', "backend"),
        Vacancy('Разработчик Python.', 'url', '60000', 'Санкт-Петербург', "Скажем на собеседовании"),
        Vacancy('QA тестер', 'url', '70000', 'Санкт-Петербург', "Писать тесты такие как этот 24/7"),
        Vacancy('Разработчик.', 'url', '80000', 'Санкт-Петербург', "Python"),
        Vacancy('junior', 'url', '90000', 'Санкт-Петербург', "умение кодить"),
        Vacancy('Сисадмин', 'url', '100000', 'Москва', "Воскрешение сгоревших (в огне) HDD "),
        Vacancy('Разработчик Python.', 'url', '100500', 'Санкт-Петербург', 'Python, backend, программист, fullstack'),
        Vacancy('Разработчик Python.', 'url', '100500', 'Санкт-Петербург', 'Python, backend, программист, fullstack'),
    ]
    # 8 - 2 - 2
    return vacancy_list


@pytest.fixture
def parameters():
    parameters = {'platforms': ['HeadHunter'],
                  'professional_role': 'Разработчик',
                  'filter_region': 'Санкт-Петербург',
                  'top_n': 7,
                  'filter_words': ['Python', 'backend', 'программист', 'fullstack'],
                  'salary_range': '50000 - 101000',
                  'per_page': 100
                  }
    return parameters


@pytest.fixture()
def json_list_one_vac():
    json_list = [
        {'id': '94189449',
         'premium': False,
         'name': 'Инженер-программист (Python)',
         'department': None, 'has_test': False,
         'response_letter_required': False,
         'area': {'id': '14', 'name': 'Архангельск', 'url': 'https://api.hh.ru/areas/14'},
         'salary': {'from': 40000, 'to': None, 'currency': 'RUR', 'gross': False},
         'type': {'id': 'open', 'name': 'Открытая'},
         'address': {
             'city': 'Архангельск',
             'street': 'улица Павла Усова',
             'building': '12с2',
             'lat': 64.537846,
             'lng': 40.585013,
             'description': None,
             'raw': 'Архангельск, улица Павла Усова, 12с2',
             'metro': None,
             'metro_stations': [], 'id': '5648996'},
         'response_url': None,
         'sort_point_distance': None,
         'published_at': '2024-03-04T11:06:59+0300',
         'created_at': '2024-03-04T11:06:59+0300',
         'archived': False,
         'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=94189449',
         'insider_interview': None,
         'url': 'https://api.hh.ru/vacancies/94189449?host=hh.ru',
         'alternate_url': 'https://hh.ru/vacancy/94189449',
         'relations': [],
         'employer': {
             'id': '5188434',
             'name': 'ДЕЛС',
             'url': 'https://api.hh.ru/employers/5188434',
             'alternate_url': 'https://hh.ru/employer/5188434',
             'logo_urls': None,
             'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=5188434',
             'accredited_it_employer': False,
             'trusted': True},
         'snippet': {
             'requirement': 'Техническое образование. Профессиональное знание <highlighttext>Python</highlighttext>, '
                            'опыт программирования на языках высокого уровня. Знание современных средств разработки '
                            'ПО и технологий. ',
             'responsibility': 'Разработка программ, компонентов программ и программных модулей на языке '
                               '<highlighttext>Python</highlighttext>. Разработка алгоритмов управления и '
                               'взаимодействия в программах. Разработка графических пользовательских...'},
         'contacts': None,
         'schedule': {'id': 'fullDay', 'name': 'Полный день'},
         'working_days': [],
         'working_time_intervals': [],
         'working_time_modes': [],
         'accept_temporary': False,
         'professional_roles': [{'id': '96', 'name': 'Программист, разработчик'}],
         'accept_incomplete_resumes': False,
         'experience': {'id': 'noExperience', 'name': 'Нет опыта'},
         'employment': {'id': 'part', 'name': 'Частичная занятость'},
         'adv_response_url': None,
         'is_adv_vacancy': False,
         'adv_context': None}
    ]

    return json_list
