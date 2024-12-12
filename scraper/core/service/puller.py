"""
Модуль содержит классы, отвечающие за получения сырых данных о товаре от
маркетплейса (данных в формате HTML, JSON и т. д.).
"""

from json import loads
from abc import ABC, abstractmethod
from curl_cffi.requests import Session

from scraper.core.dto.dto import WebDataType, ProductLink, ProductWebData


class ProductWebDataPuller(ABC):
    """
    Интерфейс, от которого должны наследоваться классы, отвечающие за
    получение сырых данных о товаре от маркетплейса.
    """

    @abstractmethod
    def get_web_data(self, link: ProductLink) -> ProductWebData:
        """
        Абстрактный метод, принимающий ссылку на товар и возвращающий
        полученные по этой ссылке сырые данные о товаре от маркетплейса.
        """

        pass


class OzonProductWebDataPuller(ProductWebDataPuller):
    """
    Реализация интерфейса ``ProductWebDataPuller``.
    Отвечает за получение сырых данных о товаре от маркетплейса Ozon.
    """

    def get_web_data(self, link: ProductLink) -> ProductWebData:
        return self.__get_json_web_data(link)

    def __get_json_web_data(self, link: ProductLink) -> ProductWebData:
        # Для выполнения запросов используется библиотеку curl_cffi (так не срабатывает защита Ozon от ботов).
        session = Session()
        raw_data = session.get("https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=" + link.link)
        is_adults_only = False

        # Если товар имеет ограничение по возрасту, запрос отправляется повторно, но с дополнительными куками.
        json_data = loads(raw_data.content.decode())
        if json_data["layout"][0]["component"] == "userAdultModal":
            is_adults_only = True
            cookies = {"is_adult_confirmed": "true", "adult_user_birthdate": "2000-10-10"}
            raw_data = session.get(
                "https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=" + link.link,
                cookies=cookies
            )

        session.close()

        return ProductWebData(link, raw_data.content.decode(), WebDataType.JSON, is_adults_only)
