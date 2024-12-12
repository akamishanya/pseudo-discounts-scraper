"""
Модуль содержит набор классов для передачи данных между другими модулями
приложения.
"""

from enum import Enum
from decimal import Decimal
from dataclasses import dataclass


class ErrorType(Enum):
    """
    Тип ошибки, произошедшей в процессе получения данных от маркетплейса.
    """

    # Информация о товаре получена успешно.
    NONE = "NONE"

    # Логика для получения данных с маркетплейса не реализована.
    MARKETPLACE_NOT_SUPPORTED = "MARKETPLACE_NOT_SUPPORTED"


class WebDataType(Enum):
    """
    Вид данных, который отдает маркетплейс.
    """

    HTML = "HTML"
    JSON = "JSON"


@dataclass(frozen=True)
class ProductLink:
    """
    Класс-обертка для ссылок.
    """

    link: str


@dataclass(frozen=True)
class ProductWebData:
    """
    Сырые данные, полученные от маркетплейса.
    """

    # Ссылка на сам товар на маркетплейсе.
    product_link: ProductLink

    # Полученные от маркетплейса сырые данные в формате ``web_data_type``.
    web_data: str

    # Вид данных, который отдает маркетплейс.
    web_data_type: WebDataType

    # Имеет ли товар ограничение по возрасту.
    is_adults_only: bool


@dataclass(frozen=True)
class ProductDetails:
    """
    Полезная информация о товаре.
    """

    # Тип ошибки, произошедшей во время получения данных от маркетплейса.
    error_type: ErrorType

    # Название товара.
    name: str | None

    # Цена на товар.
    price: Decimal | None

    # Имеет ли товар ограничение по возрасту.
    is_adults_only: bool | None

    # Ссылка на изображение товара.
    image_link: ProductLink | None

    # Ссылка на сам товар на маркетплейсе.
    product_link: ProductLink | None
