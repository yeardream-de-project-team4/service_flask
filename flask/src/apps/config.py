import os


class Config:
    KAFKA_BROKERS = os.getenv("KAFKA_BROKERS").split(",")
class Config2:   
    API_Key = os.getenv("API_Key")