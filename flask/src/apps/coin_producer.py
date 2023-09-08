import multiprocessing as mp
import pyupbit
import datetime
from config import Config
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

    def send_message(self, msg, auto_close=False):
        try:
            future = self.producer.send(self.topic, msg)
            self.producer.flush()
            if auto_close:
                self.producer.close()
            future.get(timeout=2)
            return {"status_code": 200, "error": None}
        except Exception as exc:
            raise exc



if __name__ == "__main__":
    print("===coin producer start!!!===")
    queue = mp.Queue()
    proc = mp.Process(
        target=pyupbit.WebSocketClient,
        args=('ticker', ["KRW-BTC", "KRW-ETH", "KRW-XRP"], queue),
        daemon=True
    )
    proc.start()
    brokers = Config.KAFKA_BROKERS
    topic = "coin"
    while True:
        data = queue.get()
      
        # timestamp => korean time to str yymmddhms
        temp=str(data['trade_timestamp'])[0:10]
        ts = datetime.datetime.fromtimestamp(int(temp), datetime.timezone(datetime.timedelta(hours=9))).strftime('%y%m%d%H%M%S')

        # proccesing for db column matching 
        record ={"coin_code":data['code'],"trade_price":data['trade_price'],"trade_yymmddhms":ts,"opening_price":data['opening_price'],"high_price":data['high_price'],"low_price":data['low_price']
                ,"acc_volume":data['acc_trade_volume'],"acc_price":data['acc_trade_price'],"acc_ask_volume":data['acc_ask_volume'],"acc_bid_volume":data['acc_bid_volume']}
        
        print(record)
        producer = MessageProducer(brokers, topic)
        result = producer.send_message(record)
        
        
        