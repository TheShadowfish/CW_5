import requests
from abc import ABC, abstractmethod


class AbstractApiNoAuth(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями
    """

    # @abstractmethod
    # def __init__(self, url: str, api_key: str, *parameters: tuple[str]):
    #     pass

    @abstractmethod
    def get_request(self, **parameters: dict[str: str]) -> str:
        pass


class HhApi(AbstractApiNoAuth):
    """
    Класс для работы с API сервиса hh.ru
    """

    def __init__(self, url: str = 'https://api.hh.ru/'):
        self.__url = url
        self.__last_parameters = []
        self.__last_sub_url = ''
        self.found = 0
        self.pages = 0
        self.page = 0
        self.per_page = 0

    def get_request(self, sub_url: str = 'vacancies', **parameters: dict[str: str]) -> list[dict]:
        # URL = 'https://api.hh.ru/vacancies'

        res = requests.get(self.__url + sub_url, params=parameters)
        if res.status_code != 200:
            raise Exception(f"Request code= {res.status_code}, request='{self.__url}{sub_url}', params={parameters}")

        self.__last_parameters = parameters
        self.__last_sub_url = sub_url
        self.found = res.json()['found']
        self.pages = res.json()['pages']
        self.page = res.json()['page']
        self.per_page = res.json()['per_page']

        return res.json()['items']

    def get_request_next_page(self) -> list[dict]:
        # URL = 'https://api.hh.ru/vacancies'

        if self.pages < self.page:
            self.page += 1
            self.__last_parameters['page'] = self.page
        else:
            ValueError("No more pages to request!")

        res = requests.get(self.__url + self.__last_sub_url, params=self.__last_parameters)
        if res.status_code != 200:
            raise Exception(f"Request code= {res.status_code}, request='{self.__url}{sub_url}', params={parameters}")

        self.found = res.json()['found']
        self.pages = res.json()['pages']
        self.page = res.json()['page']
        self.per_page = res.json()['per_page']

        return res.json()['items']


    def get_request_area(self, sub_url: str = 'areas', area_name: str = 'Москва') -> str | None:
        """
        Dозврат ID по имени населенного пункта или области
        """
        res = requests.get(self.__url + sub_url)

        if res.status_code != 200:
            raise Exception(f"Request code= {res.status_code}, request='{self.__url}{sub_url}'")

        # print(f"Request code= {res.status_code}, request='self.__url + sub_url'")

        area = res.json()

        result = self.recursive_find_area_id(area, area_name)

        return result

    @staticmethod
    def recursive_find_area_id(areas, area_name) -> int | None:
        """
        Найти в древовидной структуре словаря areas (HH.ru) искомый город
        """
        for area in areas:
            if area['name'] == area_name:
                return area['id']
            elif isinstance(area['areas'], list) and len(area['areas']) > 0:
                result = HhApi.recursive_find_area_id(area['areas'], area_name)
                if result is not None:
                    return result
            else:
                continue
        else:
            return None
