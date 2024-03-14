# import requests
# from typing import Dict, List

from src.api_interaction import HhApi
from src.vacancy import Vacancy
from src.connectors import VacancyJsonConnector


def user_interaction(test: bool = False):
    what_to_do = input(f" Сделать запрос с HH.ru (1) \n Загрузить вакансии из файла (2) \n "
                       f"Загрузить из файла и отфильтровать (3) \n Выход (4) \n")



    # vacancy_list = []

    if what_to_do == '1':
        vacancy_list = get_request(user_input(test), test)
    elif what_to_do == '2':
        vacancy_list = open_file()
    elif what_to_do == '3':
        vacancy_list = apply_filters(user_input(test), open_file())
    else:
        exit(0)

    [print(f"{i}) {v}") for i, v in enumerate(vacancy_list, start=1)]

    while True:

        what_to_do = input(f" Отфильтровать (1) \n Удалить дубликаты (2) \n"
                           f" Пере-сохранить в файл (3) \n Добавить в файл (4)\n"
                           f" Загрузить вакансии из файла (5) \n Выход (6) \n")

        if what_to_do == '1':
            vacancy_list = Vacancy.apply_filters(vacancy_list, user_input(test))
        elif what_to_do == '2':
            vacancy_list = Vacancy.remove_duplicates(vacancy_list)
        elif what_to_do == '3':
            save_to_file(vacancy_list, True)
        elif what_to_do == '4':
            save_to_file(vacancy_list, False)
        elif what_to_do == '5':
            vacancy_list = open_file()
        elif what_to_do == '6':
            exit(0)
        else:
            pass

        [print(f"{i}) {v}") for i, v in enumerate(vacancy_list, start=1)]


def user_input(default: bool = False) -> dict[str, str | int | list[str]]:
    """
    Получение и обработка пользовательского ввода или значений по умолчанию
    """
    parameters = {'platforms': ['HeadHunter'],
                  'professional_role': 'Информационные технологии',
                  'filter_region': 'Санкт-Петербург',
                  'top_n': 10,
                  'filter_words': ['Python', 'backend', 'программист', 'fullstack'],
                  'salary_range': '0 - 300000',
                  'per_page': 100
                  }

    if not default:
        print(f"Введите необходимые параметры запроса/выбора вакансий "
              f"(отсутствие значения - параметр не используется)")
        parameters['platforms'] = ["HeadHunter"]
        parameters['professional_role'] = input("Введите специальность (область деятельности)")
        parameters['filter_region'] = input("Введите регион или город для поиска вакансий")

        top = input(f"Введите количество вакансий для вывода в топ N (default = {parameters['top_n']}): ")
        if top.isdigit():
            parameters['top_n'] = int(top)

        parameters['filter_words'] = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()

        salary_range = input("Введите диапазон зарплат (Пример: 100000 - 150000): ")  # Пример: 100000 - 150000

        salary = [int(s.strip()) for s in parameters['salary_range'].split() if s.isdigit()]
        if len(salary) != 2 or salary[0] > salary[1]:
            print(f"Неверный диапазон. Используем значение по умолчанию ({parameters['salary_range']})")
        else:
            parameters['salary_range'] = salary_range

    return parameters


def get_request(parameters, test: bool = True) -> list[Vacancy]:
    """
    platforms = parameters['platforms']
    professional_role = parameters['professional_role']
    filter_region = parameters['filter_region']
    top_n = parameters['top_n']
    filter_words = parameters['filter_words']
    salary_range = parameters['salary_range']

    vacancy_list return
    """

    # найти идентификатор региона и профессии
    # без этого получаемые данные плохо подходят для сортировки
    print(f"Get region_id and profession_id from hh.ru... "
          f"({parameters['filter_region']}, {parameters['professional_role']})")

    region_id = HhApi.get_area_id(area_name=parameters['filter_region'])
    profession_id = HhApi.get_professional_roles_id(parameters['professional_role'])

    print("Done!")

    # параметры запроса
    if test:
        parameters = {'professional_role': profession_id, 'area': 113, 'per_page': 100}
    else:
        parameters['filter_region'] = region_id
        parameters['professional_role'] = profession_id

    hh_api = HhApi(**parameters)
    print(f"Get vacation info from hh.ru... ({parameters})")
    res = hh_api.get_vacancies()
    print(f"Done!")

    # смотрим, сколько вакансий
    if test:
        print(hh_api)

    # res = hh_api.get_vacancies() - вакансии ТОЛЬКО с первой страницы результатов (page = 0)

    user_question = ' '
    if hh_api.pages > 2:
        user_question = input(f"Обработать все результаты поиска? {hh_api.found} - найдено на сайте, "
                              f"выдача {hh_api.pages} страниц по {hh_api.per_page} вакансий? y/n")

    if user_question in {'y', 'Y', 'Н', 'н', ''}:
        vacancy_list = []
        for page_request in hh_api:
            print(f"loaded... Page {hh_api.page + 1} ({hh_api.per_page} per_page) "
                  f"from {hh_api.pages}: {round((hh_api.page + 1) * 100 / hh_api.pages)} %")

            v_next_page = HhApi.return_vacancy_list_from_json(page_request)
            vacancy_list.extend(v_next_page)

        else:
            return vacancy_list
    else:
        # res = hh_api.get_vacancies()
        vacancy_list = HhApi.return_vacancy_list_from_json(res)
        return vacancy_list
        # [print(v) for v in vacancy_list]


def open_file() -> list[Vacancy]:
    json_connector = VacancyJsonConnector()

    v_list_read = json_connector.read_from_file()
    return v_list_read


def apply_filters(parameters: dict, vacancy_list: list[Vacancy]) -> list[Vacancy]:
    print(parameters)
    print(vacancy_list)
    print("under construction!")




    return vacancy_list


def save_to_file(vacancy_list, rewrite: bool = True):
    json_connector = VacancyJsonConnector()
    if rewrite:
        json_connector.write_to_file(vacancy_list)
    else:
        json_connector.append_to_file(vacancy_list)


def get_my_url_s():
    mas_str = [
        'https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/Klastery-v-poiske-vakansij',
        'https://spb.hh.ru/article/1175',
        'https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/operation/get-vacancies',
        'https://my.sky.pro/student-cabinet/stream-module/15145/course-final-work/communication'

    ]
    print(mas_str)


# начало программы
if __name__ == '__main__':
    user_interaction()
