import os
import json

from kafka import KafkaConsumer

from consumer_crawling import callback_crawling
from consumer_weather import callback_weather


class MessageConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            bootstrap_servers=os.getenv("KAFKA_BROKERS").split(","),
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            group_id=os.getenv("KAFKA_CONSUMER_GROUP"),
            enable_auto_commit=True,
        )
        self.events = {}

    def regist_event(self, topic, callback):
        self.events[topic] = callback

    def start(self):
        self.consumer.subscribe(list(self.events.keys()))
        for message in self.consumer:
            try:
                self.events[message.topic](message)
            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":
    consumer = MessageConsumer()
    consumer.regist_event("airflow-flask-crawling", callback_crawling)
    consumer.regist_event("airflow-flask-weather", callback_weather)
    consumer.start()
