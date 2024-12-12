"""
В приложении используется паттерн абстрактная фабрика для удобного
добавления новых маркетплейсов
(см. https://refactoring.guru/ru/design-patterns/abstract-factory).

Модуль содержит интерфейс абстрактной фабрики, а также фабрики для
конкретных маркетплейсов.
"""

from abc import ABC, abstractmethod

from scraper.core.service.puller import ProductWebDataPuller, OzonProductWebDataPuller
from scraper.core.service.scraper import ProductDetailsScraper, OzonProductDetailsScraper


class MarketplaceFactory(ABC):
    """
    Интерфейс, от которого должны наследоваться фабрики для конкретных
    маркетплейсов.
    """

    @abstractmethod
    def get_product_web_data_puller(self) -> ProductWebDataPuller:
        pass

    @abstractmethod
    def get_product_details_scraper(self) -> ProductDetailsScraper:
        pass


class OzonFactory(MarketplaceFactory):
    """
    Фабрика для маркетплейса Ozon.
    """

    def get_product_web_data_puller(self) -> ProductWebDataPuller:
        return OzonProductWebDataPuller()

    def get_product_details_scraper(self) -> ProductDetailsScraper:
        return OzonProductDetailsScraper()
