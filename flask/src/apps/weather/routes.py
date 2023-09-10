import xml.etree.ElementTree as ET

import requests
from flask import jsonify
from flask import render_template

from apps.weather import blueprint
from apps.config import Config
from apps.producer import MessageProducer

messages = []


@blueprint.route("/")
def index():
    return render_template("weather_index.html", messages=messages)


@blueprint.route("test")
def test():
    return "test page"


@blueprint.route("/do/<num>", methods=["POST"])
def do(num):
    producer = MessageProducer()
    try:
        # XML 데이터를 가져오기 위한 API 요청
        url = "http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList"

        params = {
            "serviceKey": Config.WEATHER_API_Key,
            "pageNo": "1",
            "numOfRows": str(num),
            "dataType": "XML",
            "dataCd": "ASOS",
            "dateCd": "HR",
            "startDt": "20230101",
            "startHh": "01",
            "endDt": "20230901",
            "endHh": "01",
            "stnIds": "108",
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            # API 응답이 성공인 경우 XML 데이터 파싱
            xml_data = response.text
            root = ET.fromstring(xml_data)

            # 원하는 데이터 추출 및 처리
            for item in root.iter("item"):
                tm = item.find("tm").text
                ta = item.find("ta").text
                rn = item.find("rn").text
                # 데이터 처리 및 Kafka로 전송 등 필요한 작업 수행
                # 처리가 완료되면 Kafka로 메시지 전송
                data = {"temp": ta, "time": tm, "rain": rn if rn else 0}
                producer.send_message(
                    "flask-postgres-weather", data, auto_close=False
                )
                producer.send_message(
                    "flask-elk-weather", data, auto_close=False
                )
                messages.append(data)
            producer.close()
            return jsonify(data), 200
        else:
            # API 요청 실패 처리
            return "API 요청 실패", 500

    except Exception as e:
        return str(e), 500
