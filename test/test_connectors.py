import pytest

from src.connectors import JsonConnector
from src.connectors import CsvConnector
from src.connectors import TxtConnector


def test__init(test_filters):
    json_v_connector = JsonConnector()
    assert json_v_connector is not None
    csv_v_connector = CsvConnector()
    assert csv_v_connector is not None
    txt_v_connector = TxtConnector()
    assert txt_v_connector is not None


def test_write_read(test_filters):
    json_v_connector = JsonConnector('test.json')
    csv_v_connector = CsvConnector('test.csv')
    txt_v_connector = TxtConnector('test.txt')

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
    json_v_connector = JsonConnector()
    csv_v_connector = CsvConnector()
    txt_v_connector = TxtConnector()

    with pytest.raises(FileNotFoundError):
        assert json_v_connector.read_from_file('not_found.json')
    json_v_connector = JsonConnector()
    with pytest.raises(FileNotFoundError):
        assert csv_v_connector.read_from_file('not_found.json')
    json_v_connector = JsonConnector()
    with pytest.raises(FileNotFoundError):
        assert txt_v_connector.read_from_file('not_found.json')
