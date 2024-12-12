"""
Модуль содержит классы, отвечающие за получение полезных данных о товаре
из сырых данных.
"""

from re import match
from json import loads
from decimal import Decimal
from abc import ABC, abstractmethod

from scraper.core.dto.dto import ErrorType, WebDataType, ProductLink, ProductWebData, ProductDetails


class ProductDetailsScraper(ABC):
    """
    Интерфейс, от которого должны наследоваться классы, отвечающие за
    получение полезных данных о товаре из сырых данных.
    """

    @abstractmethod
    def get_details(self, web_data: ProductWebData) -> ProductDetails:
        """
        Абстрактный метод, принимающий на вход сырые данные о товаре и
        возвращающий полезные данные о нем.
        """

        pass


class OzonProductDetailsScraper(ProductDetailsScraper):
    """
    Реализация интерфейса ``ProductDetailsScraper``.
    Отвечает за получение полезных данных о товаре на маркетплейсе Ozon.
    """

    def get_details(self, web_data: ProductWebData) -> ProductDetails:
        if web_data.web_data_type == WebDataType.JSON:
            return self.__get_details_from_json(web_data)

        def __get_details_from_json(web_data: ProductWebData) -> ProductDetails:
            json_data = loads(web_data.web_data)

            name = json_data["seo"]["title"]
            name_match = match(r"^(.*?)\s+купить на OZON по низкой цене", name)
            if name_match:
                name = name_match.group(1)

            price = Decimal(loads(json_data["seo"]["script"][0]["innerHTML"])["offers"]["price"])

            image_link = ProductLink(loads(json_data["seo"]["script"][0]["innerHTML"])["image"])

            return ProductDetails(
                ErrorType.NONE,
                name,
                price,
                web_data.is_adults_only,
                image_link,
                web_data.product_link
            )
