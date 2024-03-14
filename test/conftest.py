import pytest

from src.vacancy import Vacancy


@pytest.fixture
def empty_vacancy():
    return Vacancy(None, None, None, None, None)


@pytest.fixture
def salary_real_vacancy():
    return Vacancy('Разработчик в зоопарк.', 'https://moscowzoo.ru/', '100500999', 'Москва',
                   "Необходимо умение GNUть антилоп и гладить манула (не кусь!). Опыт по взаимодействию с python'ом "
                   "обязателен.")

@pytest.fixture
def second_real_vacancy():
    return Vacancy('Разработчик Python.', 'ссылка на сайт', '100500', 'Санкт-Петербург',
                   "Много разного")

@pytest.fixture
def first_real_vacancy():
    return Vacancy('Разработчик Python.', 'ссылка на сайт', '100500', 'Санкт-Петербург',
                   "Много разного")

@pytest.fixture
def serialized_second_real_vacancy():
    return {'_Vacancy__name': 'Разработчик Python.', '_Vacancy__url': 'ссылка на сайт', '_Vacancy__salary': 100500,
            '_Vacancy__region': 'Санкт-Петербург', '_Vacancy__requirements': "Много разного"}