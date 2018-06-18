import urllib.request
import urllib.parse
from xml.etree import ElementTree

loopFlag = 1

def printMenu():
    print("******************************************************")
    print("                 대기오염 검색 APP                      ")
    print("                      Menu                             ")
    print("             1. 시도별 대기오염 정보 검색                ")
    print("             2. 세부 지역 대기오염 정보 검색             ")
    print("             3. 지도로 대기오염 정보 검색                ")
    print("******************************************************")

def SelectMenu(menu):
    if menu == '1':
        placesearch()
    elif menu == '2':
        detail_placesearch()
    elif menu == '3':
        MapSearch()
        #지도로 대기오염 정보 검색
    else:
        print("잘못된 값을 입력하셨습니다.")

def MapSearch():
    map_osm = folium.Map(location = [37.568477, 126.981611],zoom_start=13)
    folium.Marker([37.568477, 126.981611], popup='Mt. Hood Meadows').add_to(map_osm)
    map_osm.save('osm.html')

    reader = csv.reader(open('시군구별_실시간_평균정보_조회.csv', 'r'), delimiter="," )

    svg = open('')


def detail_placesearch():
    global CityList
    global placelist
    global n

    placelist = []


    CityList = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종']

    CityList = []
    CityList = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종']

    #CityList = [서울, 부산, 대구, 인천, 광주, 대전, 울산, 경기, 강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주, 세종]
    place = eval(input('도시를 선택하세요 : {0}'.format(CityList)))
    trans_place = urllib.parse.quote_plus(place)
    key = '=u6gWf4hX%2FqPazPKbDjPWntYuufDTcONxlxtmymo%2F3VhDV92yP41s7dJYuiCKwODnvOflyT8MRLXKcmlgmTz9ww%3D%3D&numOfRows=40&pageSize=10&pageNo=1&startPage=1&sidoName='
    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey' + key + trans_place + '&ver=1.3'
    data = urllib.request.urlopen(url).read()
    root = ElementTree.fromstring(data)

    for child in root.iter('item'):
        placelist.append(child.find('stationName').text)

    detail_place = input('세부지역을 입력하세요{0}'.format(placelist))
    result = detail_place + " 지역의 대기측정 값 정보입니다.\n"

    for child in root.iter('item'):
        p_name = child.find('stationName').text
        if(detail_place == p_name):
            time = child.find('dataTime').text
            name = child.find('stationName').text
            so2 = child.find('so2Value').text
            co = child.find('coValue').text
            o3 = child.find('o3Value').text
            no2 = child.find('no2Value').text
            pm10 = child.find('pm10Value').text
            n = '지역 : ' + name + '\nSo2 측정량 : ' + so2 + '\nCo 측정량 : ' + co + '\nO3 측정량 : ' + o3 + '\nNo2 측정량 : ' + no2 + '\n미세먼지 : ' + pm10 + \
                '\n=======================================================\n'
            result += n


    if (len(result) < 30):
        print("존재하지 않는 지역입니다.")
    else:
        print(time)
        print(result)


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

    if(len(result) < 100):
        print("존재하지 않는 지역입니다.")
    else:
        print(time)
        print(result)

while(loopFlag > 0):
    printMenu()
    menukey = input("메뉴를 선택해주세요 : ")
    SelectMenu(menukey)
else:
    print("프로그램 종료")