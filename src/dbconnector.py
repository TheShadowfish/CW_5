import psycopg2

"""Скрипт для заполнения данными таблиц в БД Postgres."""
import os
import csv
from src.connectors import LoadWrite, UniversalFileConnector

class DBManager(UniversalFileConnector, LoadWrite):
    """
    Имеются уникальные объекты

    Vacancy
    self.__name = valid_data['name']
    self.__url = valid_data['url']
    self.__salary = valid_data['salary']

    self.__region = valid_data['region'] - список регионов, данные повторяются
    self.__requirements = valid_data['requirements']

    self.__employer_id = valid_data['employer_id']

    Employer
    self.__id = valid_data['id']
    self.__name = valid_data['name']
    self.__url = valid_data['url']
    self.__vacancies_url = valid_data['vacancies']

    """


    def generate_bd_script():
        """
        Имеются уникальные объекты
        Vacancy         valid_data = self.validation(name=name, url=url, salary=salary,
                                     region=region, requirements=requirements,
                                     employer_id=employer_id)
        self.__name = valid_data['name']
        self.__url = valid_data['url']
        self.__salary = valid_data['salary']

        # self.__salary_from = valid_data['salary_from']
        # self.__salary_to = valid_data['salary_to']

        self.__region = valid_data['region']
        self.__requirements = valid_data['requirements']

        self.__employer_id = valid_data['employer_id']
        Employer

        """
    pass

def load_list_from_file(self, file) -> list:
        pass

def write_list_to_file(self, my_list: list, file):
        pass

def script_in_main_py(write_bd: bool):
    """
    Написать скрипт в main.py, который заполнит созданные таблицы данными из north_data
    Для подключения к БД использовать библиотеку psycopg2.
    Зайти в pgAdmin и убедиться, что данные в таблицах есть.
    """
    if write_bd:
        # customers_data
        data_list = read_from_file("customers_data.csv")
        write_to_database("customers_data", data_list)
        # employees_data
        data_list = read_from_file("employees_data.csv")
        write_to_database("employees_data", data_list)
        # orders_data
        data_list = read_from_file("orders_data.csv")
        write_to_database("orders_data", data_list)

    print_database_table("customers_data")
    print_database_table("employees_data")
    print_database_table("orders_data")



def read_from_file(filename: str = '') -> dict:
    """
    Загружает информацию из файла csv в папке north_data
    filename - название файла
    list[] - возвращает список словарей
    """
    filepath = os.path.join('north_data', filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"file {filepath} not found!")
        data_csv = []
    with open(filepath) as my_csv:
        reader = csv.DictReader(my_csv)
        data_csv = list(reader)
    return data_csv


def print_database_table(tablename):
    conn_params = {
        "host": "localhost",
        "database": "north",
        "user": "postgres",
        "password": "12345"
    }
    print(f"\n Таблица в базе north(localhost) {tablename}: \n")

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            # cur.execute("INSERT INTO mytable VALUES (%s, %s, %s)", (4, name, description))
            cur.execute(f"SELECT * FROM {tablename}")
            rows = cur.fetchall()
            for row in rows:
                print(row)
    conn.close()


def write_to_database(tablename, cvs_data: list[dict]):
    conn_params = {
        "host": "localhost",
        "database": "north",
        "user": "postgres",
        "password": "12345"
    }
    # количество параметров VALUES в INSERT INTO, т.е. (%s, %s, ... %s)
    string_s = ', '.join(['%s' for i in range(len(cvs_data[0]))])

    # превращает числовые значения в числа, строковые не меняет
    int_from_str = lambda x: int(x) if x.isdigit() else x
    # список кортежей для cur.executemany
    tuple_string = [tuple([int_from_str(v) for v in line.values()]) for line in cvs_data]

    conn2 = psycopg2.connect(**conn_params)
    cur = conn2.cursor()
    # print(f"INSERT INTO {tablename} VALUES ({string_s}) {tuple_string}")

    try:
        cur.executemany(f"INSERT INTO {tablename} VALUES ({string_s})", tuple_string)
    except Exception as e:
        print(f'Ошибка: {e}')
    else:
        # если запрос без ошибок - заносим в БД
        conn2.commit()
    finally:
        cur.close()
        conn2.close()


# начало программы
if __name__ == '__main__':
    script_in_main_py(True)

