import os
import json
from abc import ABC, abstractmethod
from src.vacancy import Vacancy
import csv


class VacancyFileConnector(ABC):
    """
    Чтение и запись вакансий в файл
    """

    @abstractmethod
    def read_from_file(self, filename: str) -> list[Vacancy]:
        pass

    @abstractmethod
    def write_to_file(self, vacancy_list: list[Vacancy]):
        pass

    @abstractmethod
    def append_to_file(self, vacancy_list: list[Vacancy]):
        pass


class VacancyJsonConnector(VacancyFileConnector):

    def __init__(self, filename: str = "vacancy.json"):
        self.__filename = filename

    def read_from_file(self, filename: str = '') -> list[Vacancy]:
        """
        Загружает информацию файла vacancy.json в папке data(по умолчанию)
        filename - название файла
        list[Vacancy] - возвращает список вакансий
        """
        if filename == '':
            filename = self.__filename

        filepath = os.path.join('data', filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"file {filepath} not found!")

        vacancy_list = []
        with open(filepath, "rt") as read_file:
            data_json = json.load(read_file)

            for vacancy in data_json:
                v = Vacancy.deserialize(vacancy)

                vacancy_list.append(v)

        return vacancy_list

    def write_to_file(self, vacancy_list: list[Vacancy]):
        """
        Пишет в файл vacancy.json в директории data
        Добавляет данные в конец файла
        """
        # относительный путь - в папке data запускаемого проекта
        filepath = os.path.join('data', self.__filename)

        # if os.path.exists(filepath):
        #     print(filepath)

        dictionary_list = [v.serialize() for v in vacancy_list]

        try:
            with open(filepath, "wt") as write_file:
                json.dump(dictionary_list, write_file)

        except OSError as e:
            print(f"Something went wrong. I can't write \"{filepath}\", {str(e)}")
        # finally:
        #     return success

    def append_to_file(self, vacancy_list: list[Vacancy]):
        """
        Пишет в файл vacancy.json в директории data
        Добавляет данные в конец файла
        """
        # относительный путь - в папке data запускаемого проекта
        filepath = os.path.join('data', self.__filename)

        file_v_list = self.read_from_file()
        file_v_list.extend(vacancy_list)

        self.write_to_file(file_v_list)


class VacancyCsvConnector(VacancyFileConnector):

    def __init__(self, filename: str = "vacancy.csv"):
        self.__filename = filename

    def read_from_file(self, filename: str = '') -> list[Vacancy]:
        """
        Загружает информацию файла vacancy.json в папке data(по умолчанию)
        filename - название файла
        list[Vacancy] - возвращает список вакансий
        """
        if filename == '':
            filename = self.__filename

        filepath = os.path.join('data', filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"file {filepath} not found!")

        vacancy_list = []

        with open(filepath) as my_csv:
            reader = csv.reader(my_csv)
            vacancy_strings = list(reader)
            with open(filepath, "wt", newline='') as write_file:
                writer = csv.DictWriter(write_file, fieldnames=dictionary_list[0])
                writer.writeheader()
                writer.writerows(dictionary_list)

            # [print(f"\t {w[0]} -> \t {w[1]}  \t {w[2]}  \t {w[3]}  \t {w[4]}") for w in word_list]
            #
            # print(f"START\n\n")
            #
            # right = 0

        for vacancy in vacancy_strings:
            v = Vacancy.deserialize(vacancy)
            vacancy_list.append(v)



        return vacancy_list

    def write_to_file(self, vacancy_list: list[Vacancy]):
        """
        Пишет в файл vacancy.json в директории data
        Добавляет данные в конец файла
        """
        # относительный путь - в папке data запускаемого проекта
        filepath = os.path.join('data', self.__filename)

        # if os.path.exists(filepath):
        #     print(filepath)

        dictionary_list = [v.serialize() for v in vacancy_list]

        try:
            with open(filepath, "wt", newline='') as write_file:
                writer = csv.DictWriter(write_file, fieldnames=dictionary_list[0])
                writer.writeheader()
                writer.writerows(dictionary_list)
                # print('I write csv!!')

        except OSError as e:
            print(f"Something went wrong. I can't write \"{filepath}\", {str(e)}")

    def append_to_file(self, vacancy_list: list[Vacancy]):
        """
        Пишет в файл vacancy.json в директории data
        Добавляет данные в конец файла
        """
        # относительный путь - в папке data запускаемого проекта
        filepath = os.path.join('data', self.__filename)

        file_v_list = self.read_from_file()
        file_v_list.extend(vacancy_list)

        self.write_to_file(file_v_list)
