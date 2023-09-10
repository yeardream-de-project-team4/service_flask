import os
import requests
from kafka import KafkaConsumer
import json


class MessageConsumer:
    def __init__(self, brokers, topics, group_id):
        self.consumer = KafkaConsumer(
            bootstrap_servers=brokers,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            group_id=group_id,
            enable_auto_commit=True,
        )
        self.consumer.subscribe(topics)

    def receive_message(self):
        try:
            for message in self.consumer:
                # Kafka로부터 받은 메시지를 HTTP POST 요청의 body로 사용
                num = message.value["num"]  # {'num': '20'}
                requests.post(f"http://haproxy:80/taehoon/do/{num}")
                print(message)
        except Exception as exc:
            raise exc


if __name__ == "__main__":
    brokers = os.getenv("KAFKA_BROKERS").split(",")
    group_id = os.getenv("KAFKA_CONSUMER_GROUP")
    topics = ["send-message-topic"]
    cs = MessageConsumer(brokers, topics, group_id)
    cs.receive_message()
