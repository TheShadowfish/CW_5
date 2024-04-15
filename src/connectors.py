import os
import json
from abc import ABC, abstractmethod
from src.vacancy import Vacancy, Employer
import csv


class AbsoluteFileConnector(ABC):
    """
    Чтение и запись вакансий в файл
    """

    @abstractmethod
    def read_from_file(self) -> list[Vacancy]:
        pass

    @abstractmethod
    def read_employers_from_file(self) -> list[Employer]:
        pass

    @abstractmethod
    def write_to_file(self, vacancy_list: list[Vacancy], employer_list: list[Employer]):
        pass

    @abstractmethod
    def append_to_file(self, vacancy_list: list[Vacancy], employer_list: list[Employer]):
        pass


class LoadWrite(ABC):
    @abstractmethod
    def load_list_from_file(self, file) -> list:
        pass

    @abstractmethod
    def write_list_to_file(self, my_list: list, file):
        pass


class UniversalFileConnector(ABC):
    def __init__(self, file_extension: str):
        self.file_extension = file_extension
        self.__filename = 'vacancy' + "." + self.file_extension
        self.__employers = 'employers' + "." + self.file_extension

    def read_from_file(self) -> list[Vacancy]:
        """
        Загружает информацию из файла vacancy в папке data
        list[Vacancy] - возвращает список вакансий
        """
        filepath = os.path.join('data', self.__filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"file {filepath} not found!")

        vacancy_list = []

        data_list = self.load_list_from_file(filepath)

        for vacancy in data_list:
            v = Vacancy.deserialize(vacancy)
            vacancy_list.append(v)

        return vacancy_list

    @abstractmethod
    def load_list_from_file(self, file) -> list:
        pass

    @abstractmethod
    def write_list_to_file(self, my_list: list, file):
        pass

    def read_employers_from_file(self) -> list[Employer]:
        """
        Загружает информацию файла employers в папке data(по умолчанию)
        list[Employer] - возвращает список работодателей
        """
        filepath = os.path.join('data', self.__employers)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"file {filepath} not found!")

        employer_list = []

        data_list = self.load_list_from_file(filepath)
        for employer in data_list:
            e = Employer.deserialize(employer)
            employer_list.append(e)

        return employer_list

    def write_to_file(self, vacancy_list: list[Vacancy], employer_list: list[Employer]):
        """
        Пишет в файл vacancy.json в директории data.
        Добавляет данные в конец файла
        """
        # относительный путь - в папке data запускаемого проекта
        filepath = os.path.join('data', self.__filename)
        filepath_employers = os.path.join('data', self.__employers)

        dictionary_list = [v.serialize() for v in vacancy_list]
        dictionary_list_employers = [e.serialize() for e in employer_list]

        try:
            self.write_list_to_file(dictionary_list, filepath)

        except OSError as e:
            print(f"Something went wrong. I can't write \"{filepath}\", {str(e)}")

        try:
            self.write_list_to_file(dictionary_list_employers, filepath_employers)

        except OSError as e:
            print(f"Something went wrong. I can't write \"{filepath_employers}\", {str(e)}")

    def append_to_file(self, vacancy_list: list[Vacancy], employer_list: list[Employer]):
        """
        Читает файл vacancy.json в директории data,
        добавляет к прочитанному имеющиеся вакансии,
        перезаписывает файл.
        """

        file_v_list = self.read_from_file()
        file_v_list.extend(vacancy_list)

        file_e_list = self.read_employers_from_file()
        file_e_list.extend(employer_list)

        self.write_to_file(file_v_list, file_e_list)


class JsonConnector(UniversalFileConnector, LoadWrite):

    def __init__(self):
        # self.file_extension = 'json'
        super().__init__('json')

    def load_list_from_file(self, file) -> list:
        with open(file, "rt") as read_file:
            data_json = json.load(read_file)
        return data_json

    def write_list_to_file(self, my_list: list, file):
        # input(f"file = {file}")

        with open(file, "wt") as write_file:
            json.dump(my_list, write_file)


class CsvConnector(UniversalFileConnector, LoadWrite):

    def __init__(self):
        super().__init__('csv')

    def load_list_from_file(self, file) -> list:
        with open(file) as my_csv:
            reader = csv.DictReader(my_csv)
            data_csv = list(reader)
        return data_csv

    def write_list_to_file(self, my_list: list, file):
        with open(file, "wt", newline='') as write_file:
            writer = csv.DictWriter(write_file, fieldnames=my_list[0])
            writer.writeheader()
            writer.writerows(my_list)
        print('I write csv!!')


class TxtConnector(UniversalFileConnector, LoadWrite):

    def __init__(self):
        super().__init__('txt')

    def load_list_from_file(self, file) -> list:
        vac_list = []
        with open(file, 'rt') as my_txt:
            for vacancy_line in my_txt:
                vac_dic = json.loads(str(vacancy_line.strip("\r""\n").replace("'", '"')))
                vac_list.append(vac_dic)
        return vac_list

    def write_list_to_file(self, my_list: list, file):
        with open(file, 'wt') as my_txt:
            for line in my_list:
                # for vacancy_string in dictionary_list:
                my_txt.write(str(line))
                my_txt.write('\n')
        print('I write txt!!')
