"""
Модуль содержит классы, реализующие логику работы с брокером сообщений.
"""

from logging import info as log_info, error as log_error
from confluent_kafka import Consumer, Producer

from scraper.core.dto.dto import ProductLink
from scraper.core.dto.serializer import ProductDetailsSerializer
from scraper.core.service.pipeline import ScraperPipelineService


class MessageBrokerService:
    """
    Класс, отвечающий за работу с брокером сообщений.

    Ссылки на товар приходят в консьюмер, обрабатываются, а затем
    отправляются в другое приложение через продюсер.
    """

    def __init__(self):
        self.__pipeline = ScraperPipelineService()

        # Конфигурация консьюмера.
        self.__consumer_config = {
            "bootstrap.servers": "localhost:9092",
            "group.id": "main-consumer",
            "auto.offset.reset": "earliest"
        }
        self.__consumer = Consumer(self.__consumer_config)
        self.__consumer.subscribe(["scraper-links-topic"])

        # Конфигурация продюсера.
        self.__producer_config = {
            "bootstrap.servers": "localhost:9092",
            "client.id": "main-producer"
        }
        self.__producer = Producer(self.__producer_config)

    def consume(self):
        """
        Метод, отвечающий за прием сообщений (ссылок) из брокера сообщений.
        """

        log_info("Consumer started")

        try:
            while True:
                log_info("Waiting for messages...")

                message = self.__consumer.poll(1.0)
                if message is None:
                    continue
                if message.error():
                    log_error(f"Consumer error: {message.error()}")
                    continue

                received = message.value().decode("utf-8")
                log_info(f"Consumer received: {received}")

                details = self.__pipeline.handle(ProductLink(received))
                json_details = ProductDetailsSerializer.to_json(details)
                log_info(f"Product details: {json_details}")

                self.__produce(json_details)
        except KeyboardInterrupt:
            pass
        finally:
            self.__consumer.close()
            log_info("Consumer stopped")

    def __produce(self, json_details: str):
        """
        Метод, отвечающий за отправку сообщений (полезных данных о товаре)
        в другое приложение через брокер сообщений.
        """

        self.__producer.produce(topic="scraper-details-topic", value=json_details, callback=self.__producer_callback)
        self.__producer.flush()

    def __producer_callback(self, error, message):
        if error:
            log_error(f"Message delivery failed: {error}")
        else:
            log_info(f"Message delivered to {message.topic()} [{message.partition()}]")
