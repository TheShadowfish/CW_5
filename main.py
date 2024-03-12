import requests
from src.api_interaction import HhApi
from src.connectors import HhVacancyConstructor


def user_interaction(userinput: bool = True):
    platforms = ["HeadHunter"]
    search_region = 'Московская область'
    top_n = 13
    # filter_words = "Python backend программист fullstack".split()
    filter_words = "Python"
    salary_range = '100000 - 150000'

    if userinput:
        platforms = ["HeadHunter"]
        search_region = input("Введите регион или город для поиска вакансий")
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
        salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    # найти идентификатор региона
    region_id = HhApi.get_area_id(area_name=search_region)

    parameters = {'text': filter_words, 'per_page': 30}

    if region_id is not None:
        parameters['area'] = str(region_id)
    else:
        print("region 'search_region' is not found, search everywhere!")

    # url уже есть по умолчанию
    # Нераспакованый словарь мы значит не берем.
    # Создание экземпляра класса для работы с платформой HH
    hh_api_hh = HhApi(**parameters)

    # res = hh_api_hh.get_vacancies()
    print(hh_api_hh)
    # print(res)

    # res = hh_api_hh.get_vacancies() - вакансии с первой страницы
    if hh_api_hh.pages < 2:
        res = hh_api_hh.get_vacancies()
    else:
        res = hh_api_hh.get_vacancies()
        user_question = input(
            f"Все результаты поиска вывести? {hh_api_hh.found} - найдено, {hh_api_hh.pages} страниц? y/n")

        if user_question in {'y', 'Y', 'Н', 'н', ''}:

            for page_request in hh_api_hh:
                print(f"\n PAGE {hh_api_hh.page} from {hh_api_hh.pages}: \n")
                for item in page_request:
                    print(item)

    vacancy_constructor = HhVacancyConstructor()
    vacancy_list = vacancy_constructor.return_vacancy_list_from_json_list(res)

    for v in vacancy_list:
        print(f"{v}")

        # print(page_request)

    # res = hh_api_hh.get_request_next_page()
    #
    # for item in res:
    #     print(item)
    #     # print_dict_recursive(item, 0)

    # area_id = 113 - регион Россия
    # Мурино: id= 5084
    # Санкт-Петербург id = 2

    # text = 'Санкт-Петербург'
    # text = 'Россия'
    # text = 'Мурино'
    # # text = 'Мухосранск'
    #
    # id1 = hh_api_hh.get_request_area(area_name=text)
    # print(f"{text}, id= {id1}")

    # res = hh_api_hh.get_request_area('areas/?area_id=Null')
    # res = hh_api_hh.get_request_area('areas/?id=1530')
    # # areas = res.json()
    # print_areas(res.json())


# def print_areas(areas):
#     for area in areas:
#         if area['name'] == 'Россия':
#             for area_rf in area['areas']:
#                 print(f"\t{area_rf['name']}: id= {area_rf['id']}")
#                 if area_rf['name'] == 'Ленинградская область' or area_rf['name'] == 'Санкт-Петербург':
#                     for area_sp in area_rf['areas']:
#                         print(f"\t\t{area_sp['name']}: id= {area_sp['id']}")
#         else:
#             print(area['name'])

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
