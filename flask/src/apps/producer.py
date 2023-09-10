import json
from kafka import KafkaProducer
from apps.config import Config


class MessageProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=Config.KAFKA_BROKERS,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
            acks=0,
            api_version=(3, 4, 1),
            retries=3,
        )

    def send_message(self, topic, msg, auto_close=True):
        try:
            future = self.producer.send(topic, msg)
            self.producer.flush()
            if auto_close:
                self.producer.close()
            future.get(timeout=2)
            return {"status_code": 200, "error": None}
        except Exception as exc:
            raise exc

    def close(self):
        self.producer.close()
