from tkinter import *
from tkinter import font
from tkinter import ttk
import urllib.request
import urllib.parse
from xml.etree import ElementTree
import folium                       #지도 연동
import mimetypes
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import tkinter.messagebox

gui = Tk()
gui.geometry("570x600+750+100")

def InitTopText():
    TempFont = font.Font(gui, size=20, weight='bold', family='Consolas')
    MainText = Label(gui, font=TempFont, text="[실시간 대기상태 검색 App]")
    MainText.place(x = 60)

def InitDetailPlaceButton():
    TempFont = font.Font(gui, size=12, weight='bold', family='Consolas')
    P_Button = Button(gui, font=TempFont, text="시도별 상세 지역 검색", command=DetailPlaceButtonAction, width=20, height=5)
    P_Button.pack()
    P_Button.place(x=20, y=120)

def DetailPlaceButtonAction():
    global ptk
    ptk = Tk()
    ptk.geometry("650x900")
    TempFont = font.Font(ptk, size=20, weight='bold', family='Consolas')
    TopText = Label(ptk, font=TempFont, text="[시도별 상세 지역 검색]")
    TopText.place(x=60)
    InitSearchListBox()
    InitInputLabel()
    InitSearchButton()
    InitListSearchButton()
    InitRenderText()
    InitListRenderText()


def InitSearchListBox():
    global CityList
    CityList = ttk.Combobox(ptk, width=15, height=20, state='readonly')
    CityList['value'] = ('서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기',
                         '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종')
    CityList.pack()
    CityList.place(x=180,y=75)
    CityList.current(0)
    TempFont = font.Font(ptk, size=15, weight='bold', family='Consolas')
    CityText = Label(ptk, text = '도시 선택', font=TempFont)
    CityText.pack()
    CityText.place(x=40,y=70)

def InitInputLabel():
    global InputLabel
    SearchFont = font.Font(ptk, size=15, weight='bold', family='Consolas')
    PlaceText = Label(ptk, font=SearchFont, text='지역 이름')
    PlaceText.place(x=40, y=450)
    TempFont = font.Font(ptk, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(ptk, font = TempFont, width = 12, borderwidth = 12, relief = 'ridge')
    InputLabel.place(x=180, y=440)

def InitSearchButton():
    TempFont = font.Font(ptk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(ptk, font = TempFont, text="검색",  command=SearchButtonAction)
    SearchButton.place(x=390, y=450)

def InitListSearchButton():
    TempFont = font.Font(ptk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(ptk, font = TempFont, text="검색",  command=ListSearchButtonAction)
    SearchButton.place(x=390, y=80)

def SearchButtonAction():
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)

    SearchPlace()

    RenderText.configure(state='disabled')

def ListSearchButtonAction():
    ListRenderText.configure(state='normal')
    ListRenderText.delete(0.0, END)

    ShowList()

    ListRenderText.configure(state='disabled')

def SearchPlace():
    flag = True
    trans_place = urllib.parse.quote_plus(CityList.get())
    key = '=u6gWf4hX%2FqPazPKbDjPWntYuufDTcONxlxtmymo%2F3VhDV92yP41s7dJYuiCKwODnvOflyT8MRLXKcmlgmTz9ww%3D%3D&numOfRows=40&pageSize=10&pageNo=1&startPage=1&sidoName='
    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey' + key + trans_place + '&ver=1.3'
    data = urllib.request.urlopen(url).read()
    root = ElementTree.fromstring(data)

    for child in root.iter('item'):
        p_name = child.find('stationName').text
        if InputLabel.get() == p_name:
            p_time = child.find('dataTime').text
            p_so2 = child.find('so2Value').text
            p_co = child.find('coValue').text
            p_o3 = child.find('o3Value').text
            p_no2 = child.find('no2Value').text
            pm10 = child.find('pm10Value').text
            pm25 = child.find('pm25Value').text

            RenderText.insert(INSERT, '시간 : ' + p_time)
            RenderText.insert(INSERT, "\n")
            RenderText.insert(INSERT, '지역 : ' + p_name + '\nSo2 측정량 : ' + p_so2 +
                              '\nCo 측정량 : ' + p_co + '\nO3 측정량 : ' + p_o3 + '\nNo2 측정량 : '
                              + p_no2 + '\n미세먼지 : ' + pm10 + '\n초미세먼지 : ' + pm25)
            RenderText.insert(INSERT, "\n")
            RenderText.insert(INSERT, '=================================================')
            RenderText.insert(INSERT, "\n")
            flag = False
        if flag == False:
            break

def InitRenderText():
    global RenderText
    RenderTextFrame = Frame(ptk)
    RenderTextScrollbar = Scrollbar(RenderTextFrame)
    RenderTextScrollbar.pack(side='right', fill="y")
    RenderText = Text(RenderTextFrame, width=50, height=15, borderwidth=12,
                      relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderText.pack()
    RenderTextFrame.pack()
    RenderTextFrame.place(x=40, y=510)
    RenderText.configure(state='disabled')

def InitListRenderText():
    global ListRenderText
    ListRenderTextFrame = Frame(ptk)
    ListRenderTextScrollbar = Scrollbar(ListRenderTextFrame)
    ListRenderTextScrollbar.pack(side='right', fill="y")
    ListRenderText = Text(ListRenderTextFrame, width=50, height=15, borderwidth=12,
                      relief='ridge', yscrollcommand=ListRenderTextScrollbar.set)
    ListRenderTextScrollbar.config(command=ListRenderText.yview)
    ListRenderText.pack()
    ListRenderTextFrame.pack()
    ListRenderTextFrame.place(x=40, y=150)
    ListRenderText.configure(state='disabled')

def ShowList():
    trans_place = urllib.parse.quote_plus(CityList.get())
    key = '=u6gWf4hX%2FqPazPKbDjPWntYuufDTcONxlxtmymo%2F3VhDV92yP41s7dJYuiCKwODnvOflyT8MRLXKcmlgmTz9ww%3D%3D&numOfRows=40&pageSize=10&pageNo=1&startPage=1&sidoName='
    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey' + key + trans_place + '&ver=1.3'
    data = urllib.request.urlopen(url).read()
    root = ElementTree.fromstring(data)

    ListRenderText.insert(INSERT, CityList.get() + "의 지역 목록입니다.\n")
    n = 0
    for child in root.iter('item'):
        p_name = child.find('stationName').text
        ListRenderText.insert(INSERT, '[' + p_name + ']' + " ")
        n += 1
        if n % 4 == 0:
            ListRenderText.insert(INSERT, '\n')

def InitAllPlaceButton():
    TempFont = font.Font(gui, size=12, weight='bold', family='Consolas')
    P_Button = Button(gui, font=TempFont, text="시도별 전체 지역 검색", command=AllPlaceButtonAction, width=20, height=5)
    P_Button.pack()
    P_Button.place(x=250, y=120)

def InitAllSearchListBox():
    global CityList
    CityList = ttk.Combobox(atk, width=15, height=20, state='readonly')
    CityList['value'] = ('서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기',
                         '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종')
    CityList.pack()
    CityList.place(x=180,y=75)
    CityList.current(0)
    TempFont = font.Font(atk, size=15, weight='bold', family='Consolas')
    CityText = Label(atk, text = '도시 선택', font=TempFont)
    CityText.pack()
    CityText.place(x=40,y=70)

def InitAllSearchButton():
    TempFont = font.Font(atk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(atk, font = TempFont, text="검색",  command=AllSearchButtonAction)
    SearchButton.place(x=390, y=70)

def AllSearchButtonAction():
    AllRenderText.configure(state='normal')
    AllRenderText.delete(0.0, END)

    AllSearchPlace()

    AllRenderText.configure(state='disabled')

def AllSearchPlace():
    trans_place = urllib.parse.quote_plus(CityList.get())
    key = '=u6gWf4hX%2FqPazPKbDjPWntYuufDTcONxlxtmymo%2F3VhDV92yP41s7dJYuiCKwODnvOflyT8MRLXKcmlgmTz9ww%3D%3D&numOfRows=40&pageSize=10&pageNo=1&startPage=1&sidoName='
    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey' + key + trans_place + '&ver=1.3'
    data = urllib.request.urlopen(url).read()
    root = ElementTree.fromstring(data)

    for child in root.iter('item'):
        p_name = child.find('stationName').text
        p_time = child.find('dataTime').text
        p_so2 = child.find('so2Value').text
        p_co = child.find('coValue').text
        p_o3 = child.find('o3Value').text
        p_no2 = child.find('no2Value').text
        pm10 = child.find('pm10Value').text
        pm25 = child.find('pm25Value').text

        AllRenderText.insert(INSERT, '시간 : ' + p_time)
        AllRenderText.insert(INSERT, "\n")
        AllRenderText.insert(INSERT, '지역 : ' + p_name + '\nSo2 측정량 : ' + p_so2 +
                          '\nCo 측정량 : ' + p_co + '\nO3 측정량 : ' + p_o3 + '\nNo2 측정량 : '
                          + p_no2 + '\n미세먼지 : ' + pm10 + '\n초미세먼지 : ' + pm25)
        AllRenderText.insert(INSERT, "\n")
        AllRenderText.insert(INSERT, '=================================================')
        AllRenderText.insert(INSERT, "\n")

def InitAllRenderText():
    global AllRenderText
    AllRenderTextFrame = Frame(atk)
    AllRenderTextScrollbar = Scrollbar(AllRenderTextFrame)
    AllRenderTextScrollbar.pack(side='right', fill="y")
    AllRenderText = Text(AllRenderTextFrame, width=50, height=20, borderwidth=12,
                      relief='ridge', yscrollcommand=AllRenderTextScrollbar.set)
    AllRenderTextScrollbar.config(command=AllRenderText.yview)
    AllRenderText.pack()
    AllRenderTextFrame.pack()
    AllRenderTextFrame.place(x=40, y=210)
    AllRenderText.configure(state='disabled')

def AllPlaceButtonAction():
    global atk
    atk = Tk()
    atk.geometry("650x700")
    TempFont = font.Font(atk, size=20, weight='bold', family='Consolas')
    TopText = Label(atk, font=TempFont, text="[시도별 전체 지역 검색]")
    TopText.place(x=60)

    InitAllSearchListBox()
    InitAllSearchButton()
    InitAllRenderText()

def InitMapButton():
    TempFont = font.Font(gui, size=12, weight='bold', family='Consolas')
    P_Button = Button(gui, font=TempFont, text="지도 검색", command=AllPlaceButtonAction, width=20, height=5)
    P_Button.pack()
    P_Button.place(x=20, y=250)

def Email():
    # global value
    host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
    port = "587"
    htmlFileName = "AirInfo.html"

    senderAddr = "yjm9494@gmail.com"  # 보내는 사람 email 주소.
    recipientAddr = "wlsaud3232@naver.com"  # 받는 사람 email 주소.

    msg = MIMEBase("multipart", "alternative")
    msg['Subject'] = "대기상태 정보"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    # MIME 문서를 생성합니다.
    htmlFD = open(htmlFileName, 'rb')
    HtmlPart = MIMEText(htmlFD.read(), 'html', _charset='UTF-8')
    htmlFD.close()

    # 만들었던 mime을 MIMEBase에 첨부 시킨다.
    msg.attach(HtmlPart)

    # 메일을 발송한다.
    s = mysmtplib.MySMTP(host, port)
    # s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("yjm9494@gmail.com", "wlsaud94")
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()

InitTopText()
InitDetailPlaceButton()
InitAllPlaceButton()
InitMapButton()

gui.mainloop()