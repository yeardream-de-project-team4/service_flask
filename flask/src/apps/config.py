import os


class Config:
    KAFKA_BROKERS = os.getenv("KAFKA_BROKERS").split(",")
    MINIO_HOST = os.getenv("MINIO_HOST")
    MINIO_USER = os.getenv("MINIO_USER")
    MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
