import requests
from src.api_interaction import HhApi
from src.connectors import HhVacancyConstructor


def user_interaction(userinput: bool = True):
    platforms = ["HeadHunter"]
    professional_role = 'Информационные технологии'

    filter_region = 'Россия'
    top_n = 13
    filter_words = "Python backend программист fullstack".split()
    # filter_words = "Разработчик"
    salary_range = '100000 - 150000'

    if userinput:
        platforms = ["HeadHunter"]
        filter_region = input("Введите регион или город для поиска вакансий")
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
        salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    # найти идентификатор региона и профессии
    # без этого получаемые данные плохо подходят для сортировки
    region_id = HhApi.get_area_id(area_name=filter_region)
    profession_id = HhApi.get_professional_roles_id(professional_role)
    print(profession_id)

    roles = HhApi.get_professional_roles()
    for r in roles['categories']:
        print(r)

    # параметры запроса
    # parameters = {'professional_role': str(profession_id), 'area': region_id,'per_page': 100}
    parameters = {'professional_role': profession_id,'per_page': 100}


    # Создание экземпляра класса для работы с платформой HH
    # if platforms != 'HeadHunter':
    #     raise NotImplementedError("Иные платформы, кроме 'HeadHunter' пока не поддерживаются.")

    hh_api_hh = HhApi(**parameters)
    res = hh_api_hh.get_vacancies()

    # смотрим, сколько вакансий
    if not userinput: print(hh_api_hh)

    #vacancy_costructor
    vacancy_constructor = HhVacancyConstructor()

    # res = hh_api_hh.get_vacancies() - вакансии ТОЛЬКО с первой страницы результатов (page = 0)
    if hh_api_hh.pages < 2:
        # res = hh_api_hh.get_vacancies()
        vacancy_list = vacancy_constructor.return_vacancy_list_from_json_list(res)
        [print(v) for v in vacancy_list]
    else:
        # res = hh_api_hh.get_vacancies()
        user_question = input(
            f"Обработать все результаты поиска? {hh_api_hh.found} - найдено, {hh_api_hh.pages} страниц? y/n")

        if user_question in {'y', 'Y', 'Н', 'н', ''}:
            vacancy_list = []
            for page_request in hh_api_hh:
                print(f"\n PAGE {hh_api_hh.page} from {hh_api_hh.pages}: \n")
                # for item in page_request:
                v_next_page = vacancy_constructor.return_vacancy_list_from_json_list(page_request)
                vacancy_list.extend(v_next_page)

                    # print(item)
                [print(v) for v in v_next_page]
        else:
            res = hh_api_hh.get_vacancies()
            vacancy_list = vacancy_constructor.return_vacancy_list_from_json_list(res)
            [print(v) for v in vacancy_list]




def print_dict_recursive(dictionary, i):
    i += 1
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print(f"{' ' * (i - 1)}{key} =")
            print_dict_recursive(value, i)
        elif isinstance(value, list) and len(value) > 0:
            print(f"{' ' * (i - 1)}{key} = \n[")
            for l in value:
                print_dict_recursive(l, i)
                print(f"{' ' * (i - 1)}{l}")
            print(f"]\n")
        else:
            print(f"{' ' * (i - 1)}{key} = {value}")
    # return questionlist
    # resdict = dict(res.json())


def get_my_urlls():
    mas_str = [
        'https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/Klastery-v-poiske-vakansij',
        'https://spb.hh.ru/article/1175',
        'https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/operation/get-vacancies',
        'https://my.sky.pro/student-cabinet/stream-module/15145/course-final-work/communication'

    ]
    print(mas_str)


# начало программы
if __name__ == '__main__':
    user_interaction(False)
