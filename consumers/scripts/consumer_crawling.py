import os
import json
import requests
from kafka import KafkaConsumer


brokers = os.getenv("KAFKA_BROKERS").split(",")
group_id = os.getenv("airflow-crawler-group")
topics = ["airflow-crawling-msg"]
consumer = KafkaConsumer(
    bootstrap_servers=brokers,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    group_id=group_id,
    enable_auto_commit=True,
)
consumer.subscribe(topics)

for message in consumer:
    ticker = message.value["ticker"]
    requests.post(f"http://haproxy:80/crawl/ticker/{ticker}")
