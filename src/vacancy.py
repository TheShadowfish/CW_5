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

    __slots__ = ('__name', '__url', '__salary', '__region', '__requirements',
                 '__employer_id', '__region_id', '__vacancy_id')

    def __init__(self, name: str, url: str, salary: str, region: str, requirements: str,
                 employer_id: str, region_id: str, vacancy_id: str):
        valid_data = self.validation(name=name, url=url, salary=salary,
                                     region=region, requirements=requirements,
                                     employer_id=employer_id, region_id=region_id, vacancy_id=vacancy_id)
        self.__name = valid_data['name']
        self.__url = valid_data['url']
        self.__salary = valid_data['salary']

        # self.__salary_from = valid_data['salary_from']
        # self.__salary_to = valid_data['salary_to']

        self.__region = valid_data['region']
        self.__requirements = valid_data['requirements']

        self.__employer_id = valid_data['employer_id']

        self.__region_id = valid_data['region_id']

        self.__vacancy_id = valid_data['vacancy_id']

        # employer_id  string  Идентификатор   работодателя.Можно   указать    несколько    значений

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

    @property
    def region_id(self):
        return self.__region_id

    @property
    def employer_id(self):
        return self.__employer_id

    @property
    def vacancy_id(self):
        return self.__vacancy_id

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

        # if isinstance(kwargs['employer_id'], str) and kwargs['employer_id'].isdigit() :
        #     raise ValueError('Идентификатор работодателя должен быть числом')
        # else:
        kwargs['employer_id'] = int(kwargs['employer_id'])

        kwargs['region_id'] = int(kwargs['region_id'])
        kwargs['vacancy_id'] = int(kwargs['vacancy_id'])

        return kwargs

    @property
    def __dict__(self) -> dict:
        """
        Использование __slots__ ломает обращение к __dict__ который был бы полезен в контексте дальнейшего
        изменения класса и добавления новых аттрибутов. Чтобы не переписывать его во всех функциях, создаем
        словарь из параметров класса.
        При изменении и добавлении параметров в класс эту функцию ОБЯЗАТЕЛЬНО нужно переписывать
        _Vacancy__name: Разработчик в зоопарк.
        _Vacancy__url: https://moscowzoo.ru/
        _Vacancy__salary: 100500999
        _Vacancy__region: Москва
        _Vacancy__requirements: Необходимо умение GNUть антилоп и гладить манула. Опыт по взаимодействию с python'ом.
        __Vacancy__employeer_id: 100500999
        PS: Даже если так в коде делать нельзя, мне об этом не говорили.
        """
        artificial_dict = {'_Vacancy' + str(self.__slots__[0]): self.__name,
                           '_Vacancy' + str(self.__slots__[1]): self.__url,
                           '_Vacancy' + str(self.__slots__[2]): self.__salary,
                           '_Vacancy' + str(self.__slots__[3]): self.__region,
                           '_Vacancy' + str(self.__slots__[4]): self.__requirements,
                           '_Vacancy' + str(self.__slots__[5]): self.__employer_id,
                           '_Vacancy' + str(self.__slots__[6]): self.__region_id,
                           '_Vacancy' + str(self.__slots__[7]): self.__vacancy_id}

        # Чтобы избежать ошибок, положим грабельки сразу.
        assert len(artificial_dict) == len(self.__slots__)

        return artificial_dict

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
        Cравнить, совпадают ли ID вакансии
        Ни за что не поверить, но описание вакансии отдается c Hh фрагментарно и зависит от запроса.
        Ну хоть по ID можно сравнить.
        """
        if not isinstance(other, Vacancy):
            raise TypeError(f"{type(other)} is not a Vacancy exemplar!")

        if self.__vacancy_id != other.__vacancy_id:
            # print(f"self.__vacancy_id == other.__vacancy_id: {self.__vacancy_id} != {other.__vacancy_id}")
            return False
        #
        # for s, o in zip(other.__dict__.items(), self.__dict__.items()):
        #     if s != o:
        #         return False
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


class Employer:
    """
        Класс для работы с компаниями (работодателями).
        Атрибуты:
        - id работодателя
        - название работодателя
        - ссылка на страницу работодателя на сайте hh
        - ссылка на вакансии

        Класс валидирует данные, которыми инициализируются его атрибуты.


        """

    __slots__ = ('__id', '__name', '__url', '__vacancies_url')

    def __init__(self, employer_id: int, name: str, url: str, vacancies: str):
        valid_data = self.validation(id=employer_id, name=name, url=url, vacancies=vacancies)
        self.__id = valid_data['id']
        self.__name = valid_data['name']
        self.__url = valid_data['url']
        self.__vacancies_url = valid_data['vacancies']

        # employeer_id = ['employer']['id']
        # name = elem['employer']['name']
        # url = elem['employer']['alternate_url']
        # vacancies_url = elem['employer']['vacancies_url']

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def vacancies(self):
        return self.__vacancies_url

    @staticmethod
    def validation(**kwargs) -> dict:
        """
        Валидация данных при создании экземпляра класса
        """
        none_text = 'Не указано'
        # 0 или Зарплата не указана
        if kwargs['id'] is not None:
            kwargs['id'] = int(kwargs['id'])
        else:
            raise ValueError('Идентификатор работодателя должен быть числом')

        if kwargs['name'] is None:
            kwargs['name'] = none_text
        if kwargs['url'] is None:
            kwargs['url'] = none_text
        if kwargs['vacancies'] is None:
            kwargs['vacancies'] = none_text
        return kwargs

    @property
    def __dict__(self) -> dict:
        """
        Использование __slots__ ломает обращение к __dict__ который был бы полезен в контексте дальнейшего
        изменения класса и добавления новых аттрибутов. Чтобы не переписывать его во всех функциях, создаем
        словарь из параметров класса.
        При изменении и добавлении параметров в класс эту функцию ОБЯЗАТЕЛЬНО нужно переписывать
        _Vacancy__name: Разработчик в зоопарк.
        _Vacancy__url: https://moscowzoo.ru/
        _Vacancy__salary: 100500999
        _Vacancy__region: Москва
        _Vacancy__requirements: Необходимо умение GNUть антилоп и гладить манула. Опыт по взаимодействию с python'ом.
        PS: Даже если так в коде делать нельзя, мне об этом не говорили.
        """
        artificial_dict = {'_Employer' + str(self.__slots__[0]): self.__id,
                           '_Employer' + str(self.__slots__[1]): self.__name,
                           '_Employer' + str(self.__slots__[2]): self.__url,
                           '_Employer' + str(self.__slots__[3]): self.__vacancies_url}

        # Чтобы избежать ошибок, положим грабельки сразу.
        assert len(artificial_dict) == len(self.__slots__)

        return artificial_dict

    def __repr__(self):
        repr_list = [str(i[0]) + ': ' + str(i[1]) for i in self.__dict__.items()]
        return f"<{self.__class__.__name__}({', '.join(repr_list)})>"

    def __str__(self):
        repr_list = [str(i[0]) + ': ' + str(i[1]) for i in self.__dict__.items()]
        delimiter = '\n\t'
        return f"Работодатель: {delimiter}{delimiter.join(repr_list)}"

    def serialize(self):
        dict_employer = {key: value for (key, value) in self.__dict__.items()}
        return dict_employer

    @classmethod
    def deserialize(cls, dict_employer):
        e = cls(*dict_employer.values())
        return e

    def is_duplicate(self, other) -> bool:
        """
        Cравнить, совпадают ли ID работодателя
        """
        if not isinstance(other, Employer):
            raise TypeError(f"{type(other)} is not a Employer exemplar!")

        if self.__id == other.__id:
            return True
        else:
            return False

    @staticmethod
    def remove_duplicates(employer_list: list) -> list:
        different_employer = []
        for e in employer_list:
            for e_checked in different_employer:
                if e.is_duplicate(e_checked):
                    break
            else:
                different_employer.append(e)

        return different_employer
