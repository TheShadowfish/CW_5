import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # <-- ADD THIS LINE

# import os
# import csv
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

    def print_database_table(self, table_number=0):
        if len(self.__tables) < table_number < len(self.__tables):
            raise ValueError(f"В базе только {len(self.__tables)} таблицы: {self.__tables}.")
        print(f"\n Таблица в базе {self.__db_name}(localhost) {self.__tables[table_number]}: \n")
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {self.__tables[table_number]}")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        conn.close()

    def write_to_file(self, vacancy_list: list[Vacancy], employer_list: list[Employer], append_only_new_data=False):
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

        # регионы

        # так короче
        regions = list(set([(int(v.region_id), v.region) for v in vacancy_list]))

        # а так быстрее должно работать
        # regions = []
        # for v in vacancy_list:
        #     for v_checked in regions:
        #         if (int(v.region_id), v.region) == v_checked:
        #             break
        #     else:
        #         regions.append((int(v.region_id), v.region))

        # работодатели
        employers = [(int(e.id), e.name, e.url, e.vacancies) for e in employer_list]

        # вакансии
        vacancies = [(int(v.vacancy_id), v.name, v.url, int(v.salary), int(v.region_id),
                      int(v.employer_id), v.requirements) for v in vacancy_list]

        # затирает всю базу данных?
        if not append_only_new_data:
            if input("Вы уверенны, что стоит стереть все данные из базы?") != 'Y':
                append_only_new_data = True

        if append_only_new_data:
            regions = self.checked_tables(regions, self.__tables[0])
            employers = self.checked_tables(employers, self.__tables[1])
            vacancies = self.checked_tables(vacancies, self.__tables[2])

        else:
            print(f"Мы такого делать не будем, у нас пока стиралка не работает.")
            return

        # в данном случае конечно пишет таблицу в БД. Хотя она тоже в итоге файл, или несколько?
        self.write_list_to_file(regions, 'regions')
        self.write_list_to_file(employers, 'employers')
        self.write_list_to_file(vacancies, 'vacancies')

    def write_list_to_file(self, my_list: list, file):
        """
        my_list - список вставляемых в БД строк
        file - название таблицы, куда вставляем
        """
        tuple_string = my_list
        tablename = file
        if len(tuple_string) == 0:
            print(f"{tablename} не содержит новых данных, не имеющихся в базе данных. Пропускаем.")
            return

        string_s = ', '.join(['%s' for i in range(len(tuple_string[0]))])
        conn2 = psycopg2.connect(**self.conn_params)
        cur = conn2.cursor()
        # print(f"INSERT INTO {tablename} VALUES ({string_s}) {tuple_string}")

        try:
            cur.executemany(f"INSERT INTO {tablename} VALUES ({string_s})", tuple_string)
        except Exception as e:
            print(f'\n ОШИБКА: {e} при записи следующего:')
            print(f"INSERT INTO {tablename} VALUES ({string_s}) {tuple_string}")
            input(f'Ошибка, ознакомьтесь! Программа продолжит работу после нажатия Enter. \n')
        else:
            # если запрос без ошибок - заносим в БД
            conn2.commit()
        finally:
            cur.close()
            conn2.close()

    def load_list_from_file(self, file) -> list:
        """
        list содержит данные запроса
        file - описание того, что будем получать (Vacancy, Employers)
        """
        if file == 'Vacancy':
            # Vacancy(self, name: str, url: str, salary: str, region: str, requirements: str,
            #                  employer_id: str, region_id: str, vacancy_id: str)

            request = 'SELECT\
             vacancies.name, url, salary, region_name, requirements, employer_id, region_id, vacancy_id\
             FROM vacancies JOIN regions USING (region_id);'

        elif file == 'Employer':
            # Employer(self, id: int, name: str, url: str, vacancies: str)
            # Запрос:
            request = 'SELECT * FROM employers;'

        else:
            raise NotImplementedError(f"{file} != (Vacancy | Employer)")

        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(request)
                rows = cur.fetchall()

                new_table = [row for row in rows]
                # for row in rows:
                #     newtable.append(row)

        conn.close()
        # [print(line) for line in new_table]
        # input("SEE///")
        return new_table


    def read_from_file(self) -> list[Vacancy]:
        """
        Загружает информацию из файла vacancy в папке data
        list[Vacancy] - возвращает список вакансий
        """
        vacancy_list = [Vacancy(*line) for line in self.load_list_from_file('Vacancy')]

        return vacancy_list

    def read_employers_from_file(self) -> list[Employer]:
        """
        Загружает информацию файла employers в папке data(по умолчанию)
        list[Employer] - возвращает список работодателей
        """
        employer_list = [Employer(*line) for line in self.load_list_from_file('Employer')]
        return employer_list

    def append_to_file(self, vacancy_list: list[Vacancy], employer_list: list[Employer]):
        """
        Читает файл базу данных PostgreSQL,
        добавляет к прочитанному вакансии и работодателей, которых не было.
        """
        self.write_to_file(vacancy_list, employer_list, append_only_new_data=True)

    def checked_tables(self, table, table_name) -> list:
        if table_name not in self.__tables:
            raise ValueError(f"В базе только {len(self.__tables)} таблицы: {self.__tables}.")

        print(f"\n Таблица в базе {self.__db_name}(localhost) {table_name}: \n")
        with psycopg2.connect(**self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {table_name}")
                rows = cur.fetchall()

                newtable = []
                for line in table:
                    for row in rows:
                        if line[0] == row[0]:
                            print(f"совпадение с БД!: {row} == {line}")
                            break
                    else:
                        newtable.append(line)

        conn.close()
        # [print(line) for line in newtable]
        # input("SEE///")
        return newtable




if __name__ == '__main__':
    dbm = DBManager()
