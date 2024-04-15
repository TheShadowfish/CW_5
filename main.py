from src.api_interaction import HhApi
from src.vacancy import Vacancy, Employer

from src.connectors import JsonConnector, CsvConnector, TxtConnector, UniversalFileConnector
from src.dbconnector import DBManager


def user_interaction():
    work_with_postgress = False

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
        file_connector = DBManager()
        work_with_postgress = True
    else:
        file_connector = DBManager()
        work_with_postgress = True

    info_big_dict = get_vacancy_data(file_connector)

    vacancy_list = info_big_dict['vacancy']
    employees_list = info_big_dict['employees']
    print("        В А К А Н С И И       ")
    [print(f"{i}) {v}") for i, v in enumerate(vacancy_list, start=1)]

    print("        Р А Б О Т О Д А Т Е Л И        ")
    [print(f"{i}) {v}") for i, v in enumerate(employees_list, start=1)]

    # what_to_do = input("\nПолучение готовых данных для PostgreSQL:"
    #                    "(Запрос с HH.ru по вакансиям, доп. запросы по работодателям, удаление дубликатов) (1) \n"
    #                    "Сделать запрос с HH.ru по вакансиям + работодатели + выбрать параметры поиска (2) \n"
    #                    "Загрузить вакансии из файла (3) \n"
    #                    "Загрузить из файла и отфильтровать (4) \n")
    #
    # if what_to_do == '1':
    #     vacancy_employers = get_request_info_universal(user_input(True), api_type='HeadHunter')
    #     vacancy_list = vacancy_employers[0]
    #     employees_list = vacancy_employers[1]
    #     employees_list = Employer.remove_duplicates(employees_list)
    #
    #     all_employer_vacancy_list = []
    #
    #     len_employers_list = len(employees_list)
    #
    #     for i, e in enumerate(employees_list, start=1):
    #         print(f"Работодатель {i} из {len_employers_list} ({i * 100 // len_employers_list}%)")
    #         e_info = HhApi.employer_get_vacancies(e.id, only_with_salary=True)
    #         all_employer_vacancy_list.extend(e_info)
    #
    #     vacancy_list.extend(all_employer_vacancy_list)
    #     vacancy_list = Vacancy.remove_duplicates(vacancy_list)
    #
    # elif what_to_do == '2':
    #     # vacancy_list = get_request_info(user_input(True), 'HeadHunter')
    #     # employees_list = get_request_info_employees(user_input(True), 'HeadHunter')
    #     vacancy_employers = get_request_info_universal(user_input(False), api_type='HeadHunter')
    #     vacancy_list = vacancy_employers[0]
    #     employees_list = vacancy_employers[1]
    #
    # elif what_to_do == '3':
    #     vacancy_list = open_file(file_connector)
    #     employees_list = open_file_employers(file_connector)
    # elif what_to_do == '4':
    #     vacancy_list = open_file(file_connector)
    #     employees_list = open_file_employers(file_connector)
    #     vacancy_list = Vacancy.apply_filters(vacancy_list, user_input(False))
    # else:
    #     exit(0)
    # print("        В А К А Н С И И       ")
    # [print(f"{i}) {v}") for i, v in enumerate(vacancy_list, start=1)]
    #
    # print("        Р А Б О Т О Д А Т Е Л И        ")
    # [print(f"{i}) {v}") for i, v in enumerate(employees_list, start=1)]

    vacancy_list = info_big_dict['vacancy']
    employees_list = info_big_dict['employees']

    if work_with_postgress:
        what_to_do = input("Выбрать режим работы с классами Vacancy, Employeer (1)\n"
                           "Выбрать режим работы с базой данных (2)\n"
                           "Выбрать выход (3)\n")
        if what_to_do == '1':
            # info_big_dict = work_with_vacancy_class(vacancy_list, employees_list, file_connector)
            # Поскольку массивы тоже меняются, допустимо просто
            work_with_vacancy_class(vacancy_list, employees_list, file_connector)
        elif what_to_do == '2':
            work_with_db(file_connector)
        elif what_to_do == '3':
            exit(0)
    else:
        # info_big_dict = work_with_vacancy_class(vacancy_list, employees_list, file_connector)
        # Поскольку массивы тоже меняются, допустимо просто
        work_with_vacancy_class(vacancy_list, employees_list, file_connector)


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


def get_vacancy_data(file_connector):
    what_to_do = input("\nПолучение готовых данных для PostgreSQL:"
                       "(Запрос с HH.ru по вакансиям, доп. запросы по работодателям, удаление дубликатов) (1) \n"
                       "Сделать запрос с HH.ru по вакансиям + работодатели + выбрать параметры поиска (2) \n"
                       "Загрузить вакансии из файла (3) \n"
                       "Загрузить из файла и отфильтровать (4) \n")

    if what_to_do == '1':
        vacancy_employers = get_request_info_universal(user_input(True), api_type='HeadHunter')
        vacancy_list = vacancy_employers[0]
        employees_list = vacancy_employers[1]
        employees_list = Employer.remove_duplicates(employees_list)

        all_employer_vacancy_list = []

        len_employers_list = len(employees_list)

        for i, e in enumerate(employees_list, start=1):
            print(f"Работодатель {i} из {len_employers_list} ({i * 100 // len_employers_list}%)")
            e_info = HhApi.employer_get_vacancies(e.id, only_with_salary=True)
            all_employer_vacancy_list.extend(e_info)

        vacancy_list.extend(all_employer_vacancy_list)
        vacancy_list = Vacancy.remove_duplicates(vacancy_list)

    elif what_to_do == '2':
        vacancy_employers = get_request_info_universal(user_input(False), api_type='HeadHunter')
        vacancy_list = vacancy_employers[0]
        employees_list = vacancy_employers[1]

    elif what_to_do == '3':
        vacancy_list = open_file(file_connector)
        employees_list = open_file_employers(file_connector)
    elif what_to_do == '4':
        vacancy_list = open_file(file_connector)
        employees_list = open_file_employers(file_connector)
        vacancy_list = Vacancy.apply_filters(vacancy_list, user_input(False))
    else:
        exit(0)
    print("        В А К А Н С И И       ")
    [print(f"{i}) {v}") for i, v in enumerate(vacancy_list, start=1)]

    print("        Р А Б О Т О Д А Т Е Л И        ")
    [print(f"{i}) {v}") for i, v in enumerate(employees_list, start=1)]

    return {'vacancy': vacancy_list, 'employees': employees_list}


def work_with_vacancy_class(vacancy_list: list[Vacancy], employees_list: list[Employer], file_connector):
    while True:

        what_to_do = input(" Отфильтровать (1) \n Удалить дубликаты (2) \n"
                           " Пере-сохранить в файл (3) \n Добавить в файл (4)\n"
                           " Загрузить вакансии из файла (5) \n"
                           " Удалить конкретную вакансию (вакансии) из списка (6) \n"
                           " Запрос информации о вакансиях работодателя из списка (7) \n"
                           " Вакансии всех работодателей (8) \n"
                           " Выход БЕЗ СОХРАНЕНИЯ (9) \n"
                           " СОХРАНИТЬ результаты и выйти (10) \n")

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
                if input("Удалить? Y(Enter)/N") in ['Y', '', 'y']:
                    vacancy_list = [v for num, v in enumerate(vacancy_list, start=1) if num not in v_list]

        elif what_to_do == '7':
            e_list = verify_list(input("Номер работодателей, вакансии которых вы хотите получить"), len(employees_list))
            print(e_list)

            if e_list:
                e_print = [employer for number, employer in enumerate(employees_list, start=1) if number in e_list]
                print("Информация по вакансиям: ")
                e_info = []

                chosen_employer_vacancy_list = []
                for e in e_print:
                    e_info = HhApi.employer_get_vacancies(e.id)
                    chosen_employer_vacancy_list.extend(e_info)

                    print("Информация по полученным вакансиям: ")
                    print(f"Работодатель: {e}, \n Вакансии: \n")
                    [print(f"{i}){v}") for i, v in enumerate(e_info, start=1)]

        elif what_to_do == '8':
            len_employers_list = len(employees_list)
            all_employer_vacancy_list = []

            for i, e in enumerate(employees_list, start=1):
                print(f"Работодатель {i} из {len_employers_list} ({i * 100 // len_employers_list}%)")
                e_info = HhApi.employer_get_vacancies(e.id, only_with_salary=True)
                all_employer_vacancy_list.extend(e_info)

            vacancy_list.extend(all_employer_vacancy_list)

        elif what_to_do == '9':
            break
        elif what_to_do == '10':
            save_to_file(vacancy_list, employees_list, file_connector, True)
            return
        else:
            break

        print("        В А К А Н С И И       ")
        [print(f"{i}) {v}") for i, v in enumerate(vacancy_list, start=1)]

        print("        Р А Б О Т О Д А Т Е Л И        ")
        [print(f"{i}) {v}") for i, v in enumerate(employees_list, start=1)]

    return {'vacancy': vacancy_list, 'employees': employees_list}


def work_with_db(file_connector):
    while True:
        what_to_do = input(" Таблица vacancies (1) \n"
                           " Таблица employers (2) \n"
                           " Таблица regions (3) \n"
                           " Удалить все вакансии из БД, где не указана зарплата (4) \n"
                           " Удалить конкретную вакансию (вакансии) из БД (5) \n"
                           " Получает список всех компаний и количество вакансий у каждой компании (6) \n"
                           " Получает список всех вакансий с указанием названия компании,"
                           " названия вакансии и зарплаты и ссылки на вакансию. (7) \n"
                           " Получает среднюю зарплату по вакансиям. (8) \n"
                           " Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. (9) \n"
                           " Получает список всех вакансий, в названии которых содержатся переданные в метод слова,"
                           "например python. (10) \n"
                           "Выход (11) \n")

        if what_to_do == '1':
            file_connector.print_database_table(2)
        elif what_to_do == '2':
            file_connector.print_database_table(1)
        elif what_to_do == '3':
            file_connector.print_database_table(0)
        elif what_to_do == '4':
            file_connector.delete_vacancies_with_zero_salary()
        elif what_to_do == '5':
            print("Список вакансий")
            file_connector.print_database_table(2)
            user_input_vacancy_id = input("Выбирайте ID вакансий, которые можно удалить, ввод через пробел")
            delete_by_id = [v_id for v_id in user_input_vacancy_id.split(' ') if v_id.isdigit()]
            file_connector.delete_vacancies_by_id(delete_by_id)

        elif what_to_do == '6':
            file_connector.get_companies_and_vacancies_count()
        elif what_to_do == '7':
            file_connector.get_all_vacancies()
        elif what_to_do == '8':
            file_connector.get_avg_salary()
        elif what_to_do == '9':
            file_connector.get_vacancies_with_higher_salary()
        elif what_to_do == '10':
            file_connector.get_vacancies_with_keyword(input("Введите ключевые слова через пробел").split(' '))
        elif what_to_do == '11':
            return


def get_request_info_universal(parameters_input, api_type: str = 'HeadHunter') -> [[Employer], [Vacancy]]:
    """
    Проверка параметров ввода от пользователя, создание экземпляра HhApi, передача параметров в HhApi,
    возврат результатов в списке списков
    """
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
            employer_list = []

            for page_request in hh_api:
                print(f"loaded... Page {hh_api.page + 1} ({hh_api.per_page} per_page) "
                      f"from {hh_api.pages}: {round((hh_api.page + 1) * 100 / hh_api.pages)} %")

                v_next_page = HhApi.return_vacancy_list_from_json(page_request)
                vacancy_list.extend(v_next_page)

                e_next_page = HhApi.return_employer_list_from_json(page_request)
                employer_list.extend(e_next_page)

            else:
                return [vacancy_list, employer_list]
        else:
            # res = hh_api.get_vacancies() - вакансии ТОЛЬКО с первой страницы результатов (page = 0)
            vacancy_list = HhApi.return_vacancy_list_from_json(res)
            employer_list = HhApi.return_employer_list_from_json(res)
            return [vacancy_list, employer_list]
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
