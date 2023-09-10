import os


class Config:
    KAFKA_BROKERS = os.getenv("KAFKA_BROKERS").split(",")
    API_Key = os.getenv("API_Key")
    MINIO_HOST = os.getenv("MINIO_HOST")
    MINIO_USER = os.getenv("MINIO_USER")
    MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
