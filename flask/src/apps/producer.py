from kafka import KafkaProducer
import json


class MessageProducer:
    def __init__(self, brokers, topic):
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=brokers,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
            acks=0,
            api_version=(3, 4, 1),
            retries=3,
        )

    def send_message(self, msg, auto_close=True):
        try:
            future = self.producer.send(self.topic, msg)
            self.producer.flush()
            if auto_close:
                self.producer.close()
            future.get(timeout=2)
            return {"status_code": 200, "error": None}
        except Exception as exc:
            raise exc
