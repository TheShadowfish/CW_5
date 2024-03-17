import pytest

from src.connectors import VacancyJsonConnector
from src.connectors import VacancyCsvConnector
from src.connectors import VacancyTxtConnector


def test__init(test_filters):
    json_v_connector = VacancyJsonConnector()
    assert json_v_connector is not None
    csv_v_connector = VacancyCsvConnector()
    assert csv_v_connector is not None
    txt_v_connector = VacancyTxtConnector()
    assert txt_v_connector is not None


def test_write_read(test_filters):
    json_v_connector = VacancyJsonConnector('test.json')
    csv_v_connector = VacancyCsvConnector('test.csv')
    txt_v_connector = VacancyTxtConnector('test.txt')

    # with pytest.raises(TypeError):
    #     json_v_connector.write_to_file(['vacancy', 'vacancy', 'vacancy'])

    json_v_connector.write_to_file(test_filters)
    csv_v_connector.write_to_file(test_filters)
    txt_v_connector.write_to_file(test_filters)

    assert len(json_v_connector.read_from_file()) == 10
    assert len(csv_v_connector.read_from_file()) == 10
    assert len(txt_v_connector.read_from_file()) == 10

    json_v_connector.append_to_file(test_filters)
    csv_v_connector.append_to_file(test_filters)
    txt_v_connector.append_to_file(test_filters)
    assert len(json_v_connector.read_from_file()) == 20
    assert len(csv_v_connector.read_from_file()) == 20
    assert len(txt_v_connector.read_from_file()) == 20


def test_read(test_filters):
    json_v_connector = VacancyJsonConnector()
    csv_v_connector = VacancyCsvConnector()
    txt_v_connector = VacancyTxtConnector()

    with pytest.raises(FileNotFoundError):
        assert json_v_connector.read_from_file('not_found.json')
    json_v_connector = VacancyJsonConnector()
    with pytest.raises(FileNotFoundError):
        assert csv_v_connector.read_from_file('not_found.json')
    json_v_connector = VacancyJsonConnector()
    with pytest.raises(FileNotFoundError):
        assert txt_v_connector.read_from_file('not_found.json')

    # try:
    #     json_v_connector.read_from_file()
    # except FileNotFoundError:
    #     pass
    # else:
    #     assert len(json_v_connector.read_from_file()) >= 0
