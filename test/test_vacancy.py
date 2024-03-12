import pytest


def test_vacancy__init(empty_vacancy, salary_real_vacancy):
    """ Корректность инициализации объектов класса Vacancy"""
    assert empty_vacancy.name == 'Не указано'
    assert empty_vacancy.url == 'Не указано'
    assert empty_vacancy.salary == 0
    assert empty_vacancy.region == 'Не указано'
    assert empty_vacancy.requirements == 'Не указано'

    assert salary_real_vacancy.name == 'Разработчик в зоопарк.'
    assert salary_real_vacancy.url == 'https://moscowzoo.ru/'
    assert salary_real_vacancy.salary == 100500999
    assert salary_real_vacancy.region == 'Москва'
    assert salary_real_vacancy.requirements == ("Необходимо умение GNUть антилоп и гладить манула (не кусь!). Опыт по "
                                                "взаимодействию с python'ом обязателен.")


def test_vacancy__str__repr(second_real_vacancy):
    assert second_real_vacancy.__str__() == (f'Вакансия: \n'
                                            '\t_Vacancy__name: Разработчик Python.\n'
                                            '\t_Vacancy__url: ссылка на сайт\n'
                                            '\t_Vacancy__salary: 100500\n'
                                            '\t_Vacancy__region: Санкт-Петербург\n'
                                             '\t_Vacancy__requirements: Много разного')

    assert second_real_vacancy.__repr__() == (f'<Vacancy(_Vacancy__name: Разработчик Python., '
                                            '_Vacancy__url: ссылка на сайт, '
                                            '_Vacancy__salary: 100500, _Vacancy__region: Санкт-Петербург, '
                                            '_Vacancy__requirements: Много разного)>')


def test_vacancy_is_duplicate(first_real_vacancy, second_real_vacancy, salary_real_vacancy):
    assert first_real_vacancy.is_duplicate(second_real_vacancy)
    # assert not first_real_vacancy.is_duplicate(second_real_vacancy, salary_real_vacancy)
