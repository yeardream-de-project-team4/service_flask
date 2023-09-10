import json
import requests
import time
from apps.market import blueprint
from apps.producer import MessageProducer


@blueprint.route("/")
def route_default():
    return "sample_app index"


@blueprint.route("/trade/<n>", methods=["POST"])
def trade(n):
    producer = MessageProducer()

    data = requests.get("https://api.upbit.com/v1/market/all").json()
    market_codes = [entry["market"] for entry in data]

    results = []  # 모든 결과를 저장하기 위한 리스트

    for code in market_codes[:10]:
        url = f"https://api.upbit.com/v1/trades/ticks?market={code}&count={n}"
        headers = {"accept": "application/json"}
        res = requests.get(url, headers=headers)
        data = res.json()

        if res.status_code == 200:
            try:
                # JSON 데이터 처리
                for msg in data:
                    result = producer.send_message(
                        "flask-postgres-market", msg, auto_close=False
                    )
                    producer.send_message(
                        "flask-elk-market", data, auto_close=False
                    )
                    results.append(result)
            except json.JSONDecodeError as e:
                print(f"JSON 디코딩 오류: {e}")
        else:
            print(f"서버 응답 오류: {res.status_code}")

        time.sleep(0.3)

    # Kafka 프로듀서 닫기
    producer.close()

    return results, 200
