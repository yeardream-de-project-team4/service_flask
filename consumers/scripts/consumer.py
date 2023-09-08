import os
import requests
from kafka import KafkaConsumer


class MessageConsumer:
    def __init__(self, brokers, topics, group_id):
        self.consumer = KafkaConsumer(
            bootstrap_servers=brokers,
            value_deserializer=lambda x: x.decode("utf-8"),
            group_id=group_id,
            enable_auto_commit=True,
        )
        self.consumer.subscribe(topics)

    def receive_message(self):
        try:
            for message in self.consumer:
                print(message)
        except Exception as exc:
            raise exc


if __name__ == "__main__":
    brokers = os.getenv("KAFKA_BROKERS").split(",")
    group_id = os.getenv("KAFKA_CONSUMER_GROUP")
    topics = ["test-flask-topic"]
    cs = MessageConsumer(brokers, topics, group_id)
    cs.receive_message()
