import os


class Config:
    KAFKA_BROKERS = os.getenv("KAFKA_BROKERS").split(",")
