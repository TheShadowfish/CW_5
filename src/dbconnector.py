import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # <-- ADD THIS LINE

import os
import csv
from src.connectors import LoadWrite, AbsoluteFileConnector
from decouple import config
from abc import ABC, abstractmethod
from src.vacancy import Vacancy, Employer


class DBManagerNeedToPerform(ABC):
    @abstractmethod
    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        pass

    @abstractmethod
    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        pass

    @abstractmethod
    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """

    @abstractmethod
    def get_vacancies_with_keyword(self):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        pass


class DBManager(AbsoluteFileConnector, LoadWrite):
    """
    Имеются уникальные объекты

            Vacancy - вакансии
    name, url  -  string
    salary - int

    region - string - список регионов, данные повторяются, характеризуется region_id (int)
    requirements - string (длинный текст)

    employer_id - int, связь с работодателем, многие к одному
    region_id - связь со списком регионов, многие ко многим

            Employer - работодатель
    id - int, связь с employer_id (Vacancy) - один ко многим
    name, url, vacancies_url - string
    """

    def __init__(self):
        self.file_extension = 'PostgreSQL'
        self.__db_name = 'headhunter_cw5'
        self.__tables = ('regions', 'employers', 'vacancies')
        # параметры user и password нужно конечно хранить отдельно
        # вообще для тестирования программы: user=postgres, password=12345
        self.__db_name = "headhunter_cw5"
        self.conn_params = {
            "host": "localhost",
            "database": self.__db_name,
            "user": config('DB_POSTRESQL_USER'),
            "password": config('DB_POSTRESQL_PASSWORD')}

        self.check_bd_script()

    def check_bd_script(self):
        """
        Проверим существование базы данных.
        Если ее нет, то создаем.
        """
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT * FROM employers")
                    cur.execute(f"SELECT * FROM vacancies")
                    cur.execute(f"SELECT * FROM regions")
            conn.close()
        except Exception as e:
            print(f'Исключение {e}. База данных {self.conn_params} и таблицы в ней еще не созданы')
            if input('Создать БД автоматически? Без этого дальнейшая работа будет невозможна. Y/N') != 'Y':
                exit(1)
            else:
                print(f'create {self.__db_name}...')
                self.create_headhunter_cw5_db()
                print(f'generate tables {self.__tables}...')
                self.generate_bd_script()
        else:
            print(f'База данных {self.conn_params} уже существует. Продолжаем работу.')

    def create_headhunter_cw5_db(self):
        # БД postrges должна быть в любом случае
        postgress_params = {
            "host": "localhost",
            "database": "postgres",
            "user": config('DB_POSTRESQL_USER'),
            "password": config('DB_POSTRESQL_PASSWORD')}

        con = psycopg2.connect(**postgress_params)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE
        cur = con.cursor()

        cur.execute(f'CREATE DATABASE {self.__db_name};')
        cur.close()
        con.close()
        print(f"{self.__db_name} создана! ")

    def generate_bd_script(self):
        """
        Создание БД и таблиц:
        Спроектировать таблицы в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях.
        Для работы с БД используйте библиотеку psycopg2.
        Вот здесь все таблицы и создаются, можно заценить.
        """
        create_region = "CREATE TABLE regions (region_id int UNIQUE PRIMARY KEY, region_name varchar(50) NOT NULL);"

        create_employers = "CREATE TABLE employers (\
                                    employer_id int UNIQUE PRIMARY KEY,\
                                    name varchar(200) NOT NULL,\
                                    url varchar(200) NOT NULL,\
                                    vacancies_url varchar(250) NOT NULL\
                                    );"

        # надо бы id вакансии получать с hh, лучше, чем самому автогенерировать.
        create_vacancy = "CREATE TABLE vacancies (\
                                    vacancy_id int UNIQUE PRIMARY KEY,\
                                    name varchar(200) NOT NULL,\
                                    url varchar(200) NOT NULL,\
                                    salary int,\
                                    region_id int REFERENCES regions(region_id),\
                                    employer_id int REFERENCES employers(employer_id),\
                                    requirements text\
                                    );"
        print("Подключение...")
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                # cur.execute("INSERT INTO mytable VALUES (%s, %s, %s)", (4, name, description))
                cur.execute(create_region)
                print("Таблица region создана!")
                cur.execute(create_employers)
                print("Таблица employers создана!")
                cur.execute(create_vacancy)
                print("Таблица vacancy создана!")

    def print_database_table(self, bdname, tablename):

        print(f"\n Таблица в базе {bdname}(localhost) {tablename}: \n")

        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                # cur.execute("INSERT INTO mytable VALUES (%s, %s, %s)", (4, name, description))
                cur.execute(f"SELECT * FROM {tablename}")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        conn.close()

    def write_to_file(self, vacancy_list: list[Vacancy], employer_list: list[Employer]):
        """
        Пишет в базу данных PostgreSQL информацию о работодателях и вакансиях.


            Vacancy - вакансии
        name, url  -  string
        salary - int

        region - string - список регионов, данные повторяются, характеризуется region_id (int)
        requirements - string (длинный текст)

        employer_id - int, связь с работодателем, многие к одному
        region_id - связь со списком регионов, многие ко многим

            Employer - работодатель
        id - int, связь с employer_id (Vacancy) - один ко многим
        name, url, vacancies_url - string
        """
        # # работодатели
        # create_region = "CREATE TABLE regions (region_id int UNIQUE PRIMARY KEY, region_name varchar(50) NOT NULL);"
        #
        # create_employers = "CREATE TABLE employers (\
        #                              employer_id int UNIQUE PRIMARY KEY,\
        #                              name varchar(200) NOT NULL,\
        #                              url varchar(200) NOT NULL,\
        #                              vacancies_url varchar(250) NOT NULL\
        #                              );"
        #
        # # надо бы id вакансии получать с hh, лучше, чем самому автогенерировать.
        # create_vacancy = "CREATE TABLE vacancies (\
        #                              vacancy_id int UNIQUE PRIMARY KEY,\
        #                              name varchar(200) NOT NULL,\
        #                              url varchar(200) NOT NULL,\
        #                              salary int,\
        #                              region_id int REFERENCES regions(region_id),\
        #                              employer_id int REFERENCES employers(employer_id),\
        #                              requirements text\
        #                              );"
        # int_from_str = lambda x: int(x) if x.isdigit() else x
        # список кортежей для cur.executemany
        # tuple_string = [tuple([int_from_str(v) for v in line.values()]) for line in cvs_data]

        # регионы
        regions = [{'region_id': int(v.region_id), 'region_name': v.region} for v in vacancy_list]

        # работодатели
        employers = [{'employer_id': int(e.id), 'name': e.name, 'url': e.url,
                      'vacancies_url': e.vacancies} for e in employer_list]

        # вакансии
        vacancies = [{'vacancy_id': int(v.vacancy_id), 'name': v.name, 'url': v.url, 'salary': int(v.salary),
                      'region_id': int(v.region_id), 'employer_id': int(v.employer_id),
                      'requirements': v.requirements} for v in vacancy_list]

        # в данном случае конечно пишет таблицу в БД. Хотя она тоже файл, вроде как.
        self.write_list_to_file(regions, 'regions')
        self.write_list_to_file(employers, 'employers')
        self.write_list_to_file(vacancies, 'vacancies')

    def write_list_to_file(self, my_list: list, file):
        tuple_string = my_list
        tablename = file
        string_s = ', '.join(['%s' for i in range(len(tuple_string[0]))])
        conn2 = psycopg2.connect(**self.conn_params)
        cur = conn2.cursor()
        print(f"INSERT INTO {tablename} VALUES ({string_s}) {tuple_string}")

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

    # def read_from_file(self) -> list[Vacancy]:
    #     """
    #     Загружает информацию из файла vacancy в папке data
    #     list[Vacancy] - возвращает список вакансий
    #     """

    # @abstractmethod
    # def load_list_from_file(self, file) -> list:
    #     pass
    #
    # @abstractmethod

    # def read_employers_from_file(self) -> list[Employer]:
    #     """
    #     Загружает информацию файла employers в папке data(по умолчанию)
    #     list[Employer] - возвращает список работодателей
    #     """

    # def append_to_file(self, vacancy_list: list[Vacancy], employer_list: list[Employer]):
    #     """
    #     Читает файл vacancy.json в директории data,
    #     добавляет к прочитанному имеющиеся вакансии,
    #     перезаписывает файл.
    #     """

    def read_from_file(self) -> list[Vacancy]:
        raise NotImplementedError
        pass

    def load_list_from_file(self, file) -> list:
        raise NotImplementedError
        pass

    def read_employers_from_file(self) -> list[Employer]:
        raise NotImplementedError
        pass

    def append_to_file(self, vacancy_list: list[Vacancy], employer_list: list[Employer]):
        raise NotImplementedError
        pass

    def script_in_main_py(self, write_bd: bool):
        """
        Написать скрипт в main.py, который заполнит созданные таблицы данными из north_data
        Для подключения к БД использовать библиотеку psycopg2.
        Зайти в pgAdmin и убедиться, что данные в таблицах есть.
        """
        if write_bd:
            # customers_data
            data_list = self.read_from_file("customers_data.csv")
            self.write_to_database("customers_data", data_list)
            # employees_data
            data_list = self.read_from_file("employees_data.csv")
            self.write_to_database("employees_data", data_list)
            # orders_data
            data_list = self.read_from_file("orders_data.csv")
            self.write_to_database("orders_data", data_list)

        self.print_database_table("customers_data")
        self.print_database_table("employees_data")
        self.print_database_table("orders_data")

    def read_from_file(self, filename: str = '') -> dict:
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

    def write_to_database(self, tablename, cvs_data: list[dict]):
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


if __name__ == '__main__':
    dbm = DBManager()
