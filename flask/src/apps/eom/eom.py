import json
import requests
import time
from apps.eom import blueprint
from apps.config import Config
from apps.producer import MessageProducer
from flask import request, jsonify


@blueprint.route("/")
def route_default():
    return "sample_app index"


@blueprint.route("/test")
def route_test():
    return "sample_app test22"


@blueprint.route("/say/<word>")
def route_say(word):
    return word


@blueprint.route("/send", methods=["POST"])
def upload():
    data = request.get_json()
    name = data["name"]
    age = data["age"]
    return json.dumps({name: name, age: age}), 200


@blueprint.route("/do", methods=["POST"])
def do():
    brokers = Config.KAFKA_BROKERS
    topic = "eom-topic"
    producer = MessageProducer(brokers, topic)

    # do something

    data = {"name": "mark", "age": 25}
    result = producer.send_message(data)
    return result, 200

@blueprint.route("/trade", methods=["POST"])
def trade():
    brokers = Config.KAFKA_BROKERS
    topic = "eom-topic"
    producer = MessageProducer(brokers, topic)

    url1 = "https://api.upbit.com/v1/market/all"
    res1 = requests.get(url1)
    data = res1.json()
    market_codes = [entry["market"] for entry in data]

    results = []  # 모든 결과를 저장하기 위한 리스트


    for market_code in market_codes:
        url = f"https://api.upbit.com/v1/trades/ticks?market={market_code}&count=1"
        headers = {"accept": "application/json"}
        res = requests.get(url, headers=headers)
        
        if res.status_code == 200:
            try:
                data = res.json()
                # JSON 데이터 처리
                print(data)
                for d in data:
                    result = producer.send_message(d, auto_close=False)
                    results.append(result)
            except json.JSONDecodeError as e:
                print(f"JSON 디코딩 오류: {e}")
        else:
            print(f"서버 응답 오류: {res.status_code}")
        
        time.sleep(1)

    # Kafka 프로듀서 닫기
    producer.producer.close()

    return results, 200

# def trade():
#     brokers = Config.KAFKA_BROKERS
#     topic = "eom-topic"
#     producer = MessageProducer(brokers, topic)

#     url1 = "https://api.upbit.com/v1/market/all"
#     res1 = requests.get(url1)
#     data = res1.json()
#     market_codes = [entry["market"] for entry in data]

#     for market_code in market_codes:
#         url = f"https://api.upbit.com/v1/trades/ticks?market={market_code}&count=1"
#         headers = {"accept": "application/json"}
#         res = requests.get(url, headers=headers)
#         data = res.json()
#     if res.status_code == 200:
#         try:
#             data = res.json()
#             # JSON 데이터 처리
#             print(data)
#         except json.JSONDecodeError as e:
#             print(f"JSON 디코딩 오류: {e}")
#     else:
#         print(f"서버 응답 오류: {res.status_code}")

#     for d in data:
#         result = producer.send_message(d, auto_close=False)
#         producer.producer.close()
    
#     return result, 200

    

        