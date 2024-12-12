"""
Модуль, содержащий логику по запуску приложения.
"""

from logging import basicConfig, DEBUG, StreamHandler

from scraper.core.service.broker import MessageBrokerService


def configure_logger():
    """
    Конфигурирование базового логирования в терминал.
    """

    basicConfig(
        level=DEBUG,
        format="%(asctime)s.%(msecs)03d %(levelname)-8s %(name)-5s %(filename)-10s (%(lineno)03d) : %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
        handlers=[StreamHandler()]
    )


def main():
    """
    Точка входа в скрипт.
    """

    # Конфигурирование логирования.
    configure_logger()

    # Запуск приема сообщений из брокера сообщений.
    broker = MessageBrokerService()
    broker.consume()


if __name__ == "__main__":
    main()
