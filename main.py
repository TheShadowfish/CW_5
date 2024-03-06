import requests
from src.api_hh import HhApi


def user_interaction(userinput: bool = True):
    platforms = ["HeadHunter"]
    search_query = "Введите поисковый запрос: "
    top_n = 13
    filter_words = "Python backend программист fullstack".split()
    salary_range = '100000 - 150000'

    if userinput:
        platforms = ["HeadHunter"]
        search_query = input("Введите поисковый запрос: ")
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
        salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    # filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    #
    # ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    #
    # sorted_vacancies = sort_vacancies(ranged_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # print_vacancies(top_vacancies)
    hh_api_hh = HhApi('https://api.hh.ru/')

    res = hh_api_hh.get_request('vacancies', {'text': 'Python'})

    # URL = 'https://api.hh.ru/vacancies'

    # res = requests.get(URL, params={'text': 'Python'})

    print(res.status_code)
    print(res.json())

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
