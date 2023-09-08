


# Python3 샘플 코드 #


import requests
import xml.etree.ElementTree as ET


keys = 'H+bRrYoogayH++vDw9WAUoaucWn3GoEoMCP0IDhOGWz1hAk5NLQhy3cl0JtnU2m4xSpXhnKe9oTRrjUfJ1cckA=='
url = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList'
params ={'serviceKey' : keys, 'pageNo' : '1', 'numOfRows' : '10', 'dataType' : 'XML', 'dataCd' : 'ASOS', 'dateCd' : 'HR', 'startDt' : '20230101', 'startHh' : '01', 'endDt' : '20230901', 'endHh' : '01', 'stnIds' : '108' }

response = requests.get(url, params=params)

print(response.content)
# xml 형식의 응답을 파싱합니다.
root = ET.fromstring(response.content)

# 각 요소에 대해 반복하며 정보를 출력합니다.
for item in root.iter('item'):
    
  stnId = item.find('stnId').text if item.find('stnId') is not None else ""
  tm = item.find('tm').text if item.find('tm') is not None else ""
  ta = item.find('ta').text if item.find('ta') is not None else ""

  print(f"지역 ID: {stnId}, 시간: {tm}, 온도: {ta}")