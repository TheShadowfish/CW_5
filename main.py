from src.api_interaction import HhApi
from src.vacancy import Vacancy, Employer
import requests


# from src.connectors import JsonConnector
# from src.connectors import CsvConnector
# from src.connectors import TxtConnector
from src.connectors import JsonConnector, CsvConnector, TxtConnector, UniversalFileConnector


def user_interaction():
    what_to_do = input("Выберите формат файла для сохранения данных: \n"
                       "TXT (vacancy.txt) (1) \n"
                       "CSV (vacancy.csv) (2) \n"
                       "JSON (vacancy.json) (3) \n"
                       "PostgreSQL - работа с базой данных (4) (default) \n")

    if what_to_do == '1':
        file_connector = TxtConnector()
    elif what_to_do == '2':
        file_connector = CsvConnector()
    elif what_to_do == '3':
        file_connector = JsonConnector()
    elif what_to_do == '4':
        raise NotImplementedError("ПРЯМ СРАЗУ? НЕТ.")
    else:
        file_connector = JsonConnector()

    # надоело файл выбирать
    # file_connector = JsonConnector()

    what_to_do = input(" Сделать запрос с HH.ru по вакансиям + работодатели (1) \n"
                       " Загрузить вакансии из файла (2) \n"
                       " Загрузить из файла и отфильтровать (3) \n")

    # vacancy_list = []
    # json_connector = VacancyJsonConnector()
    # csv_connector = VacancyCsvConnector()
    # txt_connector = VacancyTxtConnector()

    # employees_list = []

    if what_to_do == '1':
        vacancy_list = get_request_info(user_input(True), 'HeadHunter')
        employees_list = get_request_info_employees(user_input(True), 'HeadHunter')
    elif what_to_do == '2':
        vacancy_list = open_file(file_connector)
        employees_list = open_file_employers(file_connector)
    elif what_to_do == '3':
        vacancy_list = open_file(file_connector)
        employees_list = open_file_employers(file_connector)
        vacancy_list = Vacancy.apply_filters(vacancy_list, user_input(False))
    else:
        exit(0)
    print("        В А К А Н С И И       ")
    [print(f"{i}) {v}") for i, v in enumerate(vacancy_list, start=1)]

    print("        Р А Б О Т О Д А Т Е Л И        ")
    [print(f"{i}) {v}") for i, v in enumerate(employees_list, start=1)]

    while True:

        what_to_do = input(" Отфильтровать (1) \n Удалить дубликаты (2) \n"
                           " Пере-сохранить в файл (3) \n Добавить в файл (4)\n"
                           " Загрузить вакансии из файла (5) \n"
                           " Удалить конкретную вакансию (вакансии) из списка (6) \n"
                           " Запрос информации о вакансиях работодателя из списка (7)"
                           " Выход БЕЗ СОХРАНЕНИЯ (8) \n"
                           " СОХРАНИТЬ результаты и выйти (9) \n")

        if what_to_do == '1':
            vacancy_list = Vacancy.apply_filters(vacancy_list, user_input(False))
        elif what_to_do == '2':
            vacancy_list = Vacancy.remove_duplicates(vacancy_list)
            employees_list = Employer.remove_duplicates(employees_list)
        elif what_to_do == '3':
            save_to_file(vacancy_list, employees_list, file_connector, True)
        elif what_to_do == '4':
            save_to_file(vacancy_list, employees_list, file_connector, False)
        elif what_to_do == '5':
            vacancy_list = open_file(file_connector)
        elif what_to_do == '6':
            v_list = verify_list(input("Номера вакансий, которые вы хотите удалить (введите номера через пробел)"),
                                 len(vacancy_list))
            print(v_list)
            if v_list:
                v_deleted = [vacancy for number, vacancy in enumerate(vacancy_list, start=1) if number in v_list]
                print("Будут удалены следующие вакансии: ")
                [print(f"{v_del[0]}) {v_del[1]}") for v_del in zip(v_list, v_deleted)]
                if input("Удалить? Y/N") not in ['т', 'T', 'N', 'n']:
                    vacancy_list = [v for num, v in enumerate(vacancy_list, start=1) if num not in v_list]

        elif what_to_do == '7':
            e_list = verify_list(input("Номер работодателей, вакансии которых вы хотите получить"), len(employees_list))
            print(e_list)
            if e_list:
                e_print = [employer for number, employer in enumerate(employees_list, start=1) if number in e_list]
                print("Информация по вакансиям: ")
                e_info = []
                for e in e_print:
                    input(f"ID= {e.id}, URL={e.url}")
                    input(f"\n text= {HhApi.employer_get_vacancies(e.id, e.url)}")

                    # print(f"{e.url} :  + {HhApi.employer_text(e.url)}")

                    e_info.extend(HhApi.employer_get_vacancies(e.id, e.url))

                print("Информация по вакансиям: ")
                [print(f"{e_see[0]}) \n => {e_see[1]}") for e_see in zip(e_print, e_info)]
                # employer_get_info(employe)

                input("Ожидание реакции...")


        elif what_to_do == '8':
            exit(0)
        elif what_to_do == '9':
            save_to_file(vacancy_list, employees_list, file_connector, True)
            exit(0)
        else:
            pass

        print("        В А К А Н С И И       ")
        [print(f"{i}) {v}") for i, v in enumerate(vacancy_list, start=1)]

        print("        Р А Б О Т О Д А Т Е Л И        ")
        [print(f"{i}) {v}") for i, v in enumerate(employees_list, start=1)]


def user_input(default: bool = False) -> dict[str, str | int | list[str]]:
    """
    Получение и обработка пользовательского ввода или значений по умолчанию
    """
    parameters = {'platforms': ['HeadHunter'],
                  'professional_role': 'Информационные технологии',
                  'filter_region': 'Санкт-Петербург',
                  'top_n': 10,
                  'filter_words': ['Python', 'backend', 'программист'],
                  'salary_range': '0 - 300000',
                  'per_page': 100
                  }

    if not default:
        print("Введите необходимые параметры запроса/выбора вакансий "
              "(отсутствие значения - параметр не используется)")
        parameters['platforms'] = ["HeadHunter"]
        parameters['professional_role'] = input("Введите специальность (область деятельности)")
        parameters['filter_region'] = input("Введите регион или город для поиска вакансий")

        top = input(f"Введите количество вакансий для вывода в топ N (default = {parameters['top_n']}): ")
        if top.isdigit():
            parameters['top_n'] = int(top)

        parameters['filter_words'] = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()

        salary_range = input("Введите диапазон зарплат (Пример: 100000 - 150000): ")  # Пример: 100000 - 150000

        if salary_range == '':
            parameters['salary_range'] = salary_range
        else:
            salary = [int(s.strip()) for s in salary_range.split('-') if s.strip().isdigit()]
            # input(f'{salary}/// see')
            if len(salary) != 2 or salary[0] > salary[1]:
                print(f"Неверный диапазон. Используем значение по умолчанию ({parameters['salary_range']})")
            else:
                parameters['salary_range'] = salary_range

    return parameters


def get_request_info(parameters_input, api_type: str = 'HeadHunter') -> list[Vacancy]:
    """
    Проверка параметров ввода от пользователя, создание экземпляра HhApi, передача параметров в HhApi,
    возврат результатов в списке
    """
    # print(salary)
    if api_type not in parameters_input['platforms']:
        raise NotImplementedError(f"С платформой {api_type} взаимодействие пока не реализовано")

    if api_type == 'HeadHunter':

        parameters = HhApi.check_parameters_to_request(parameters_input)

        print(f"Parameters {parameters}")

        hh_api = HhApi(**parameters)

        print(f"Get vacation info from hh.ru... ({parameters})")
        res = hh_api.get_vacancies()
        print("Done!")

        # смотрим, сколько вакансий
        print(hh_api)

        user_question = ''
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
            # res = hh_api.get_vacancies() - вакансии ТОЛЬКО с первой страницы результатов (page = 0)
            vacancy_list = HhApi.return_vacancy_list_from_json(res)
            return vacancy_list
            # [print(v) for v in vacancy_list]


def get_request_info_employees(parameters_input, api_type: str = 'HeadHunter') -> list[Employer]:
    """
    Проверка параметров ввода от пользователя, создание экземпляра HhApi, передача параметров в HhApi,
    возврат результатов в списке
    """
    # print(salary)
    # get_employers: bool = True

    if api_type not in parameters_input['platforms']:
        raise NotImplementedError(f"С платформой {api_type} взаимодействие пока не реализовано")

    if api_type == 'HeadHunter':

        parameters = HhApi.check_parameters_to_request(parameters_input)

        print(f"Parameters {parameters}")

        hh_api = HhApi(**parameters)

        print(f"Get employers info from hh.ru... ({parameters})")
        res = hh_api.get_vacancies()
        print("Done!")

        # смотрим, сколько вакансий
        print(hh_api)

        user_question = ''
        if hh_api.pages > 2:
            user_question = input(f"Обработать все результаты поиска? {hh_api.found} - найдено на сайте, "
                                  f"выдача {hh_api.pages} страниц по {hh_api.per_page} вакансий? y/n")

        if user_question in {'y', 'Y', 'Н', 'н', ''}:
            # vacancy_list = []

            employer_list = []

            for page_request in hh_api:
                print(f"loaded... Page {hh_api.page + 1} ({hh_api.per_page} per_page) "
                      f"from {hh_api.pages}: {round((hh_api.page + 1) * 100 / hh_api.pages)} %")

                # v_next_page = HhApi.return_vacancy_list_from_json(page_request)
                # if get_employees:

                e_next_page = HhApi.return_employer_list_from_json(page_request)

                # get_employers = False

                # vacancy_list.extend(v_next_page)
                employer_list.extend(e_next_page)

            else:
                # print("see...employer_list")
                # for e in employer_list:
                #     print(e)
                # input("see...employer_list")

                return employer_list
        else:
            # res = hh_api.get_vacancies() - вакансии ТОЛЬКО с первой страницы результатов (page = 0)
            # vacancy_list = HhApi.return_vacancy_list_from_json(res)
            employer_list = HhApi.return_employer_list_from_json(res)

            # print("see...employer_list")
            # for e in employer_list:
            #     print(e)
            # input("see...employer_list")

            return employer_list
            # [print(v) for v in vacancy_list]


def verify_list(vac_numbers: str, list_length: int) -> list[int] | None:
    """
    Обрабатывает и верифицирует список номеров вакансий, которые надо удалить
    :param list_length:
    :param vac_numbers: list[int] | None:
    :return: str
    """
    try:
        vac_list = [int(v) for v in vac_numbers.split(' ')]

        # bool_sum - число вакансий, номер которых превышает длину списка
        bool_sum = sum([(v > list_length) for v in vac_list])
        if bool_sum > 0:
            print(bool_sum)
            raise IndexError
        return vac_list
    except ValueError:
        print("Ошибка ValueError. Номер/номера удаляемых вакансий должны быть числами, разделенными пробелом")
        return None
    except IndexError:
        print("Ошибка IndexError. Номер удаляемой вакансии должен быть в пределах списка вакансий")
        return None


def open_file(connector: UniversalFileConnector) -> list[Vacancy]:
    v_list_read = connector.read_from_file()
    return v_list_read


def open_file_employers(connector: UniversalFileConnector) -> list[Employer]:
    e_list_read = connector.read_employers_from_file()
    return e_list_read


def save_to_file(vacancy_list, employer_list, connector: UniversalFileConnector, rewrite: bool = True):
    if rewrite:
        connector.write_to_file(vacancy_list, employer_list)
    else:
        connector.append_to_file(vacancy_list, employer_list)


# начало программы
if __name__ == '__main__':
    user_interaction()
