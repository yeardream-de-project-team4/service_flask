import multiprocessing as mp
import pyupbit
import datetime
import os, json
from kafka import KafkaProducer

class MessageProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_BROKERS").split(","),
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

if __name__ == "__main__":
    print("===coin producer start!!!===")
    queue = mp.Queue()
    proc = mp.Process(
        target=pyupbit.WebSocketClient,
        args=("ticker", ["KRW-BTC", "KRW-ETH", "KRW-XRP"], queue),
        daemon=True,
    )
    proc.start()
    producer = MessageProducer()
    while True:
        data = queue.get()

        # timestamp => korean time to str yymmddhms
        temp = str(data["trade_timestamp"])[0:10]
        ts = datetime.datetime.fromtimestamp(
            int(temp), datetime.timezone(datetime.timedelta(hours=9))
        ).strftime("%y%m%d%H%M%S")

        # proccesing for db column matching
        record = {
            "coin_code": data["code"],
            "trade_price": data["trade_price"],
            "trade_yymmddhms": ts,
            "opening_price": data["opening_price"],
            "high_price": data["high_price"],
            "low_price": data["low_price"],
            "acc_volume": data["acc_trade_volume"],
            "acc_price": data["acc_trade_price"],
            "acc_ask_volume": data["acc_ask_volume"],
            "acc_bid_volume": data["acc_bid_volume"],
        }

        print(record)
        result = producer.send_message(
            "flask-postgres-coin", record, auto_close=False
        )
        producer.send_message("flask-elk-coin", record, auto_close=False)
