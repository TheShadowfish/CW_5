import requests
from src.api_hh import HhApi


def user_interaction(userinput: bool = True):
    platforms = ["HeadHunter"]
    search_region = 'Санкт-Петербург'
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


    # text = 'Мурино'
    # # text = 'Мухосранск'
    #
    # id1 = hh_api_hh.get_request_area(area_name=text)
    # print(f"{text}, id= {id1}")


    # filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    #
    # ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    #
    # sorted_vacancies = sort_vacancies(ranged_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # print_vacancies(top_vacancies)


    hh_api_hh = HhApi()
    #
    # text = 'Ленинградская область'
    # # text = 'Мухосранск'
    #
    # id1 = hh_api_hh.get_request_area(area_name=text)
    # print(f"{text}, id= {id1}")


    # area_id = 113 - регион Россия
    # Мурино: id= 5084
    # Санкт-Петербург id = 2

    region_id = hh_api_hh.get_request_area(area_name=search_region)

    if region_id is None:
        res = hh_api_hh.get_request(text=filter_words, per_page=50)
        print("region_id is None!")
    else:
        res = hh_api_hh.get_request(text=filter_words, area=str(region_id), per_page=5)

    # URL = 'https://api.hh.ru/vacancies'

    # res = requests.get(URL, params={'text': 'Python'})

    # print(res.status_code)
    # print(res.json())
    for item in res:
        print_dict_recursive(item, 0)

    print(f"\n\n\n NEXT PAGE \n\n\n")
    res = hh_api_hh.get_request_next_page()
    for item in res:
        print_dict_recursive(item, 0)


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
            print(f"{' ' * (i-1)}{key} =")
            print_dict_recursive(value, i)
        elif isinstance(value, list) and len(value) > 0:
            print(f"{' ' * (i - 1)}{key} = \n[")
            for l in value:
                print_dict_recursive(l, i)
                print(f"{' ' * (i - 1)}{l}")
            print(f"]\n")
        else:
            print(f"{' ' * (i-1)}{key} = {value}")
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
