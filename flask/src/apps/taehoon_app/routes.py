import json
from apps.taehoon_app import blueprint
from apps.config import Config
from apps.config import Config2

from apps.producer import MessageProducer
from flask import jsonify
from flask import render_template
import requests
import xml.etree.ElementTree as ET
from kafka import KafkaConsumer


# Kafka Consumer 설정
consumer = KafkaConsumer(
    "send-message-topic",
    bootstrap_servers=Config.KAFKA_BROKERS,
    value_deserializer=lambda x: x.decode("utf-8"),
)
# 메시지 저장을 위한 리스트
messages = []



@blueprint.route("/")
def index():
    return render_template("index.html",messages=messages)


@blueprint.route("test")
def test():
    return "test page" , Config2.API_Key
import psycopg2
from flask import render_template



@blueprint.route("/do/<num>", methods=["POST"])
def do(num):
    brokers = Config.KAFKA_BROKERS
    topic = "taehoon-topic3"
    producer = MessageProducer(brokers, topic)
    try:
        # XML 데이터를 가져오기 위한 API 요청
        url = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList'
        
        
        params = {
            'serviceKey': Config2.API_Key,
            'pageNo': '1',
            'numOfRows': str(num),
            'dataType': 'XML',
            'dataCd': 'ASOS',
            'dateCd': 'HR',
            'startDt': '20230101',
            'startHh': '01',
            'endDt': '20230901',
            'endHh': '01',
            'stnIds': '108'
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            # API 응답이 성공인 경우 XML 데이터 파싱
            xml_data = response.text
            root = ET.fromstring(xml_data)

            # 원하는 데이터 추출 및 처리
            for item in root.iter('item'):
                tm = item.find('tm').text
                ta = item.find('ta').text
                rn = item.find('rn').text
                # 데이터 처리 및 Kafka로 전송 등 필요한 작업 수행
                # 처리가 완료되면 Kafka로 메시지 전송
                data = {'temp': ta, 'time': tm, 'rain': rn if rn else 0}
                producer.send_message(data, auto_close=False)
            producer.producer.close()
            return jsonify(data), 200

        else:
            # API 요청 실패 처리
            return "API 요청 실패", 500

    except Exception as e:
        return str(e), 500
# @blueprint.route('/data')
# def data():
#     url = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList'

#     params ={'serviceKey' : keys, 'pageNo' : '1', 'numOfRows' : '10', 'dataType' : 'XML', 'dataCd' : 'ASOS', 'dateCd' : 'HR', 'startDt' : '20230101', 'startHh' : '01', 'endDt' : '20230901', 'endHh' : '01', 'stnIds' : '108' }


#     response = requests.get(url, params=params)

#     # xml 형식의 응답을 파싱합니다.
#     root = ET.fromstring(response.content)

#     data_list = []
    
#     for item in root.iter('item'):
        
#       stnId = item.find('stnId').text if item.find('stnId') is not None else ""
#       tm = item.find('tm').text if item.find('tm') is not None else ""
#       ta = item.find('ta').text if item.find('ta') is not None else ""

#       data_list.append({
#           "지역 ID": stnId,
#           "시간": tm,
#           "온도": ta
#       })

#     return render_template("index.html", data=data_list)
