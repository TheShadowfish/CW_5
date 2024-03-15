import pytest

from src.connectors import VacancyJsonConnector


def test__init(test_filters):
    json_v_connector = VacancyJsonConnector()
    assert json_v_connector is not None


def test_write(test_filters):
    json_v_connector = VacancyJsonConnector('test.json')

    # with pytest.raises(TypeError):
    #     json_v_connector.write_to_file(['vacancy', 'vacancy', 'vacancy'])

    json_v_connector.write_to_file(test_filters)
    # assert len(json_v_connector.read_from_file()) == 10

    # json_v_connector.append_to_file(test_filters)
    # assert len(json_v_connector.read_from_file()) == 20

def test_read(test_filters):
    json_v_connector = VacancyJsonConnector()
    with pytest.raises(FileNotFoundError):
        assert json_v_connector.read_from_file('not_found.json')
    try:
        json_v_connector.read_from_file()
    except FileNotFoundError:
        pass
    else:
        assert len(json_v_connector.read_from_file()) >= 0
