class Vacancy:
    """
    Класс для работы с вакансиями.
    Атрибуты:
    - название вакансии
    - ссылка на вакансию
    - зарплата
    - регион/город
    - краткое описание или требования
     Класс поддерживает методы сравнения вакансий между собой по зарплате
    Класс валидирует данные, которыми инициализируются его атрибуты.
    Способами валидации данных может быть проверка, указана или нет зарплата.
    В этом случае выставлять значение зарплаты 0 или «Зарплата не указана»
    в зависимости от структуры класса.

    """

    # __slots__ = ('__name', '__url', '__salary', '__region', '__requirements')

    def __init__(self, name: str, url: str, salary: str, region: str, requirements: str):
        valid_data = self.validation(name=name, url=url, salary=salary, region=region, requirements=requirements)
        self.__name = valid_data['name']
        self.__url = valid_data['url']
        self.__salary = valid_data['salary']
        self.__region = valid_data['region']
        self.__requirements = valid_data['requirements']

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def salary(self):
        return self.__salary

    @property
    def region(self):
        return self.__region

    @property
    def requirements(self):
        return self.__requirements

    @staticmethod
    def validation(**kwargs) -> dict:
        """
        Валидация данных при создании экземпляра класса
        """
        none_text = 'Не указано'
        # 0 или Зарплата не указана
        if kwargs['salary'] is None:
            kwargs['salary'] = 0
        else:
            kwargs['salary'] = int(kwargs['salary'])

        if kwargs['name'] is None:
            kwargs['name'] = none_text
        if kwargs['url'] is None:
            kwargs['url'] = none_text
        if kwargs['region'] is None:
            kwargs['region'] = none_text
        if kwargs['requirements'] is None:
            kwargs['requirements'] = none_text
        return kwargs

    def __repr__(self):
        repr_list = [str(i[0]) + ': ' + str(i[1]) for i in self.__dict__.items()]
        return f"<{self.__class__.__name__}({', '.join(repr_list)})>"

    def __str__(self):
        repr_list = [str(i[0]) + ': ' + str(i[1]) for i in self.__dict__.items()]
        delimiter = '\n\t'
        return f"Вакансия: {delimiter}{delimiter.join(repr_list)}"

    def serialize(self):
        dict_vacancy = {key: value for (key, value) in self.__dict__.items()}
        return dict_vacancy

    @classmethod
    def deserialize(cls, dict_vacancy):
        v = cls(*dict_vacancy.values())
        return v

    def is_duplicate(self, other) -> bool:
        """
        сравнить, совпадают ли вакансии полностью
            self.__name = other.__name
            self.__url = other.__url
            self.__salary = other.__salary
            self.__region = other.__region
            self.__requirements = other.__requirements
        """
        if not isinstance(other, Vacancy):
            raise TypeError(f"{type(other)} is not a Vacancy exemplar!")

        for s, o in zip(other.__dict__.items(), self.__dict__.items()):
            if s != o:
                return False
        else:
            return True

    @staticmethod
    def remove_duplicates(vacancy_list: list) -> list:
        different_vacancies = []
        for v in vacancy_list:
            for v_checked in different_vacancies:
                if v.is_duplicate(v_checked):
                    break
            else:
                different_vacancies.append(v)
        return different_vacancies

    @staticmethod
    def apply_filters(vacancy_list: list, parameters: dict) -> list:
        """
        :param parameters:
            parameters['platforms']
            professional_role = parameters['professional_role']
            parameters['filter_region']
            parameters['top_n']
            parameters['filter_words']
            salary_range = parameters['salary_range']
        :param vacancy_list:
        :return: filtered vacancy_list:

        self.__name = valid_data['name']
        self.__url = valid_data['url']
        self.__salary = valid_data['salary']
        self.__region = valid_data['region']
        self.__requirements = valid_data['requirements']
        """
        filtered_vacancy_list = []
        if isinstance(parameters['filter_words'], list):
            filter_list = parameters['filter_words'][:]
        else:
            filter_list = [parameters['filter_words']]
        filter_list.append(parameters['professional_role'])
        filter_list = [f for f in filter_list if f != '']
        # print(filter_list)
        # print(parameters['filter_words'])
        # print(parameters['professional_role'])

        salary = [int(s.strip()) for s in parameters['salary_range'].split() if s.isdigit()]

        for vac in vacancy_list:
            append = True

            if len(salary) == 2 and (salary[0] >= vac.salary or salary[1] <= vac.salary):
                append = False

            elif parameters['filter_region'] != '' and parameters['filter_region'] != vac.region:
                append = False

            elif len(filter_list) > 0:
                for word in filter_list:
                    if word in vac.requirements or word in vac.name:
                        break
                else:
                    append = False

            if append:
                # input(f"TRUE!!, \n {parameters} \n  {vac}? True?")
                filtered_vacancy_list.append(vac)
            else:
                pass

        return (sorted(filtered_vacancy_list, reverse=True))[0:parameters['top_n']]

    """
    Методы для операций сравнения:
    __lt__(self, other) — <;
    __le__(self, other) — <=;
    __eq__(self, other) — ==;
    __ne__(self, other) — !=;
    __gt__(self, other) — >;
    __ge__(self, other) — >=.
    для определения операций сравнения достаточно в классе определить только три метода: ==, <, <=,
    если остальные являются их симметричной противоположностью.
    В этом случае язык Python сам подберет нужный метод и выполнит его при сравнении объектов.
    """

    @classmethod
    def __verify_data(cls, other):
        if not isinstance(other, cls):
            raise TypeError(f"'{type(cls)}' can't be compared with '{type(other)}'!")

    def __eq__(self, other):
        self.__verify_data(other)
        return self.__salary == other.__salary

    def __lt__(self, other):
        self.__verify_data(other)
        return self.__salary < other.__salary

    def __le__(self, other):
        self.__verify_data(other)
        return self.__salary <= other.__salary
