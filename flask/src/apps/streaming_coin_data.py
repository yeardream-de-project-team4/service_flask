import multiprocessing as mp
import pyupbit
import datetime
from apps.producer import MessageProducer


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
