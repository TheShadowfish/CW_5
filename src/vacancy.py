class Vacancy:
    """
    Класс для работы с вакансиями.
    Атрибуты:
    - название вакансии
    - ссылка на вакансию
    - зарплата
    - краткое описание или требования
     Класс поддерживает методы сравнения вакансий между собой по зарплате
    Класси валидирует данные, которыми инициализируются его атрибуты.
    Способами валидации данных может быть проверка, указана или нет зарплата.
    В этом случае выставлять значение зарплаты 0 или «Зарплата не указана» в зависимости от структуры класса.

    """
    # __slots__ = ('__name', '__url', '__salary', '__region', '__requirements')

    def __init__(self, name: str, url: str, salary: str, region: str, requirements: str):
        valid_data = self.validation(name = name, url=url, salary = salary)
        self.__name = name
        self.__url = url
        self.__salary = valid_data['salary']
        self.__region = region
        self.__requirements = requirements

    @staticmethod
    def validation(**kwargs: dict) -> dict:
        """
        Валидация данных при создании экземпляра класса
        """
        # 0 или Зарплата не указана
        print (kwargs['salary'])
        # if (kwargs['salary'])

        # salary: 0 or from
        #<highlighttext>Python</highlighttext> убрать
        return kwargs

    def __repr__(self):
        repr_list = [str(i[0]) + ': ' + str(i[1]) for i in self.__dict__.items()]
        return f"<{self.__class__.__name__}({', '.join(repr_list)})>"
    def __str__(self):
        repr_list = [str(i[0]) + ': ' + str(i[1]) for i in self.__dict__.items()]
        delimeter = f'\n\t'
        return f"Вакансия: \n({delimeter.join(repr_list)})"


    @classmethod
    def is_duplicate(self, other) -> bool:
        """
        сравнить, совпадают ли вакансии полностью
            self.__name = other.__name
            self.__url = other.__url
            self.__salary = other.__salary
            self.__region = other.__region
            self.__requirements = other.__requirements
        """
        if isinstance(other, Vacancy):
            repr_list = [str(i[0]) + ': ' + str(i[1]) for i in self.__dict__.items()]

            for s, o in zip(self.__dict__.items(), other.__dict__.items()):
                if isinstance(s, (int, str, float, bool)) and isinstance(o, (int, str, float, bool)):
                   if s != o:
                       return False
                else:
                    raise ValueError(f"{type(s)}, {type(o)} is not immutable, now we need to change 'is_duplicate' "
                                     f"realisation in Vacancy!")
            else:
                return True
        else:
            raise TypeError(f"{type(other)} is not a Vacancy exemplar!")

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
        if not isinstance(other, (cls)):
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