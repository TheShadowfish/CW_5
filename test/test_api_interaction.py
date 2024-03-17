import pytest
from src.api_interaction import HhApi


def test_api_hh__init__(parameters):
    api_hh = HhApi('https://api.hh.ru/vacancies', **parameters)
    assert api_hh is not None

    # def __str__(self):
    #     repr_list = [str(i[0]) + ': ' + str(i[1]) for i in self.__dict__.items()]
    #     delimiter = f'\n\t'
    #     return f"{self.__class__.__name__}{delimiter}{delimiter.join(repr_list)}"
    assert api_hh.page == 0
    assert api_hh.per_page == 0
    assert api_hh.pages == 0
    assert api_hh.found is None

    sl = '{'
    sr = '}'

    assert str(api_hh) == (f'HhApi\n'
                           f'\t_HhApi__url: https://api.hh.ru/vacancies\n'
                           f"\t_HhApi__parameters: {sl}'platforms': ['HeadHunter'], 'professional_role': "
                           f"'Разработчик', 'filter_region': 'Санкт-Петербург', 'top_n': 7, "
                           f"'filter_words': ['Python', 'backend', 'программист', 'fullstack'], "
                           f"'salary_range': '50000 - 101000', 'per_page': 100{sr}\n"
                           f'\tfound: None\n'
                           f'\tpages: 0\n'
                           f'\tpage: 0\n'
                           f'\tper_page: 0'
                           )

    assert 'https://api.hh.ru/vacancies' in api_hh.__repr__()

    # assert api_hh.__iter__() == 0


def test_hh_api_get_request(parameters):
    # api_hh = HhApi(**parameters)

    assert HhApi.get_area_id('Москва') is not None
    assert HhApi.get_professional_roles_id('Информационные технологии') is not None
    assert HhApi.get_professional_roles() is not None
    # assert api_hh.get_vacancies() is not None


def test_hh_api_get_vacancies(parameters):
    api_hh = HhApi(**parameters)
    # res = api_hh.get_vacancies()
    # assert res is not None
    with pytest.raises(Exception):
        assert api_hh.get_vacancies()


def test_return_vacancy_from_json(json_list_one_vac):
    vac_list = HhApi.return_vacancy_list_from_json(json_list_one_vac)
    assert len(vac_list) > 0


def test_check_parameters_to_request(parameters):
    parameters_checked = HhApi.check_parameters_to_request(parameters)
    parameters = {'platforms': ['HeadHunter'],
                  'professional_role': 'Разработчик',
                  'filter_region': 'Санкт-Петербург',
                  'top_n': 7,
                  'filter_words': ['Python', 'backend', 'программист', 'fullstack'],
                  'salary_range': '50000 - 101000',
                  'per_page': 100
                  }

    assert parameters_checked.get('area') is not None
    assert parameters_checked.get('professional_role') != parameters['professional_role']
    assert parameters_checked.get('text') is not None
    assert parameters_checked.get('salary') is not None
    assert parameters_checked.get('only_with_salary') is not None
