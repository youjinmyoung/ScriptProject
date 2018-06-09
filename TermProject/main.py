import urllib.request
import urllib.parse
from xml.etree import ElementTree


def placesearch():
    place = input("지역이름을 입력하세요( 예) 서울, 인천 등) : ")
    trans_place = urllib.parse.quote_plus(place)
    key = '=u6gWf4hX%2FqPazPKbDjPWntYuufDTcONxlxtmymo%2F3VhDV92yP41s7dJYuiCKwODnvOflyT8MRLXKcmlgmTz9ww%3D%3D&numOfRows=40&pageSize=10&pageNo=1&startPage=1&sidoName='
    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey' + key + trans_place + '&ver=1.3'
    data = urllib.request.urlopen(url).read()
    result = place + " 지역의 대기측정 값 정보입니다.\n"
    root = ElementTree.fromstring(data)

    for child in root.iter('item'):
        time = child.find('dataTime').text
        name = child.find('stationName').text
        so2 = child.find('so2Value').text
        co = child.find('coValue').text
        o3 = child.find('o3Value').text
        no2 = child.find('no2Value').text
        pm10 = child.find('pm10Value').text

        n = '지역 : ' + name + '\nSo2 측정량 : ' + so2 + '\nCo 측정량 : ' + co + '\nO3 측정량 : ' + o3 + '\nNo2 측정량 : ' + no2 + '\n미세먼지 : ' + pm10 +\
            '\n=======================================================\n'
        result += n

    print(time)
    print(result)

placesearch()