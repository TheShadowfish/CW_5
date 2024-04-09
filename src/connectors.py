import os
import json
from abc import ABC, abstractmethod
from src.vacancy import Vacancy, Employeer
import csv


class FileConnector(ABC):
    """
    Чтение и запись вакансий в файл
    """

    @abstractmethod
    def read_from_file(self, filename: str = '') -> list[Vacancy]:
        pass

    @abstractmethod
    def read_empl_from_file(self, filename: str = '') -> list[Employeer]:
        pass

    @abstractmethod
    def write_to_file(self, vacancy_list: list[Vacancy], employeer_list: list[Employeer]):
        pass

    @abstractmethod
    def append_to_file(self, vacancy_list: list[Vacancy], employeer_list: list[Employeer]):
        pass


class LoadWrite(ABC):
    @abstractmethod
    def file_load(self, file) -> list:
        pass

    @abstractmethod
    def file_write(self, my_list: list[Vacancy | Employeer], file):
        pass


class UniversalFileConnector(FileConnector):
    def __init__(self, file_extension: str):
        self.file_extension = file_extension
        self.__filename = 'vacancy' + "." + self.file_extension
        self.__employeers = 'employeers' + "." + self.file_extension

    def read_from_file(self) -> list[Vacancy]:
        """
        Загружает информацию из файла vacancy в папке data
        list[Vacancy] - возвращает список вакансий
        """
        filepath = os.path.join('data', self.__filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"file {filepath} not found!")

        vacancy_list = []
        with open(filepath, "rt") as file:
            data_list = self.file_load(file)

            for vacancy in data_list:
                v = Vacancy.deserialize(vacancy)
                vacancy_list.append(v)
        return vacancy_list

    def file_load(self, file) -> list:
        # raise NotImplementedError("Реализация в наследниках класса")
        if self.file_extension == 'json':
            raise NotImplementedError("Реализация в наследниках класса")
            data_json = json.load(file)
            return data_json
        elif self.file_extension == 'cvs':
            raise NotImplementedError("Реализация в наследниках класса")
            reader = csv.DictReader(file)
            data_csv = list(reader)
            return data_csv
        elif self.file_extension == 'txt':
            raise NotImplementedError("Реализация в наследниках класса")
            return None
        else:
            raise NotImplementedError(f"Чтение файлов с расширением {self.file_extension} не реализовано")

    def file_write(self, my_list: list[Vacancy | Employeer], file):
        # raise NotImplementedError("Реализация в наследниках класса")
        if self.file_extension == 'json':
            json.dump(my_list, file)
        elif self.file_extension == 'cvs':
            writer = csv.DictWriter(file, fieldnames=my_list[0])
            writer.writeheader()
            writer.writerows(my_list)
        elif self.file_extension == 'txt':
            return None
        else:
            raise NotImplementedError(f"Чтение файлов с расширением {self.file_extension} не реализовано")

    def read_empl_from_file(self) -> list[Employeer]:
        """
        Загружает информацию файла employeer в папке data(по умолчанию)
        list[Employeer] - возвращает список работодателей
        """
        filepath = os.path.join('data', self.__employeers)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"file {filepath} not found!")

        employeer_list = []
        with open(filepath, "rt") as file:
            data_list = self.file_load(file)
            for employeer in data_list:
                e = Employeer.deserialize(employeer)
                employeer_list.append(e)

        return employeer_list

    def write_to_file(self, vacancy_list: list[Vacancy], employeer_list: list[Employeer]):
        """
        Пишет в файл vacancy.json в директории data.
        Добавляет данные в конец файла
        """
        # относительный путь - в папке data запускаемого проекта
        filepath = os.path.join('data', self.__filename)
        filepath_employeers = os.path.join('data', self.__employeers)

        dictionary_list = [v.serialize() for v in vacancy_list]
        dictionary_list_employeers = [e.serialize() for e in employeer_list]

        try:
            with open(filepath, "wt") as write_file:
                self.file_write(dictionary_list, write_file)

        except OSError as e:
            print(f"Something went wrong. I can't write \"{filepath}\", {str(e)}")

        try:
            with open(filepath_employeers, "wt") as write_file:
                self.file_write(dictionary_list_employeers, write_file)

        except OSError as e:
            print(f"Something went wrong. I can't write \"{filepath_employeers}\", {str(e)}")

    def append_to_file(self, vacancy_list: list[Vacancy], employeer_list: list[Employeer]):
        """
        Читает файл vacancy.json в директории data,
        добавляет к прочитанному имеющиеся вакансии,
        перезаписывает файл.
        """

        file_v_list = self.read_from_file()
        file_v_list.extend(vacancy_list)

        file_e_list = self.read_empl_from_file()
        file_e_list.extend(employeer_list)

        self.write_to_file(file_v_list, file_e_list)



class JsonConnector(UniversalFileConnector, LoadWrite):

    def __init__(self):
        # self.file_extension = 'json'
        super().__init__('json')

    def file_load(self, file) -> list:
        with open(file, "rt") as read_file:
            data_json = json.load(read_file)
        return data_json

    def file_write(self, my_list: list[Vacancy | Employeer], file):
        with open(file, "wt") as write_file:
            json.dump(my_list, write_file)


class CsvConnector(UniversalFileConnector, LoadWrite):

    def __init__(self):
        super().__init__(self, 'csv')

    def file_load(self, file) -> list:
        with open(file) as my_csv:
            reader = csv.DictReader(my_csv)
            data_csv = list(reader)
        return data_csv

    def file_write(self, my_list: list[Vacancy | Employeer], file):
        with open(file, "wt", newline='') as write_file:
            writer = csv.DictWriter(write_file, fieldnames=my_list[0])
            writer.writeheader()
            writer.writerows(my_list)
            # print('I write csv!!')


class TxtConnector(UniversalFileConnector, LoadWrite):

    def __init__(self):
        super().__init__(self, 'txt')

    def file_load(self, file) -> list:
        vacancy_list = []
        with open(file, 'rt') as my_txt:
            for vacancy_line in my_txt:
                vac_dic = json.loads(str(vacancy_line.strip("\r""\n").replace("'", '"')))

                v = Vacancy.deserialize(vac_dic)
                vacancy_list.append(v)
        return vacancy_list
    def file_write(self, my_list: list[Vacancy | Employeer], file):
        with open(file, 'wt') as my_txt:
            for line in my_list:
                # for vacancy_string in dictionary_list:
                my_txt.write(str(line))
                my_txt.write('\n')
            # print('I write csv!!')


