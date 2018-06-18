from tkinter import *
from tkinter import font
from tkinter import ttk
import urllib.request
import urllib.parse
from xml.etree import ElementTree
import tkinter.messagebox

import spam

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


gui = Tk()
gui.geometry("570x600+750+100")
photo = PhotoImage(file="cloud.gif")
imageLabel = Label(gui, image=photo)
imageLabel.pack()

def InitTopText():
    TempFont = font.Font(gui, size=20, weight='bold', family='Consolas')
    MainText = Label(gui, font=TempFont, text="[실시간 대기상태 검색 App]",bg="white")
    MainText.place(x = 60)

def InitDetailPlaceButton():
    TempFont = font.Font(gui, size=12, weight='bold', family='Consolas')
    P_Button = Button(gui, font=TempFont, text="시도별 상세 지역 검색", command=DetailPlaceButtonAction, width=20, height=2, bg="white")
    P_Button.pack()
    P_Button.place(x=170, y=120)

def DetailPlaceButtonAction():
    global ptk
    ptk = Toplevel(gui)
    ptk.geometry("570x900")
    photo = PhotoImage(file="cloud.gif")
    imageLabel = Label(ptk, image=photo)
    imageLabel.pack()
    TempFont = font.Font(ptk, size=20, weight='bold', family='Consolas')
    TopText = Label(ptk, font=TempFont, text="[시도별 상세 지역 검색]",bg="white")
    TopText.place(x=80)
    InitSearchListBox()
    InitInputLabel()
    InitSearchButton()
    InitListSearchButton()
    InitRenderText()
    InitListRenderText()
    EmailAddress()
    ptk.mainloop()

def InitSearchListBox():
    global CityList
    CityList = ttk.Combobox(ptk, width=15, height=20, state='readonly')
    CityList['value'] = ('서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기',
                         '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종')
    CityList.pack()
    CityList.place(x=180,y=75)
    CityList.current(0)
    TempFont = font.Font(ptk, size=15, weight='bold', family='Consolas')
    CityText = Label(ptk, text = '도시 선택', font=TempFont,bg="white")
    CityText.pack()
    CityText.place(x=40,y=70)

def InitInputLabel():
    global InputLabel
    SearchFont = font.Font(ptk, size=15, weight='bold', family='Consolas')
    PlaceText = Label(ptk, font=SearchFont, text='지역 이름',bg="white")
    PlaceText.place(x=40, y=450)
    TempFont = font.Font(ptk, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(ptk, font = TempFont, width = 12, borderwidth = 12, relief = 'ridge')
    InputLabel.place(x=180, y=440)

def InitSearchButton():
    TempFont = font.Font(ptk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(ptk, font = TempFont, text="검색",  command=SearchButtonAction,bg="white")
    SearchButton.place(x=390, y=450)

def InitListSearchButton():
    TempFont = font.Font(ptk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(ptk, font = TempFont, text="검색",  command=ListSearchButtonAction,bg="white")
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
    key = spam.getkey()
    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey' + key + trans_place + '&ver=1.3'
    data = urllib.request.urlopen(url).read()
    root = ElementTree.fromstring(data)

    global p_name, p_time, p_co, p_no2, p_o3, p_so2, pm10, pm25

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
            RenderText.insert(INSERT, '\n지역 : ' + p_name + '\nSo2 측정량 : ' + p_so2 +
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
    key = spam.getkey()
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
    P_Button = Button(gui, font=TempFont, text="시도별 전체 지역 검색", command=AllPlaceButtonAction, width=20, height=2,bg="white")
    P_Button.pack()
    P_Button.place(x=170, y=250)

def InitAllSearchListBox():
    global CityList
    CityList = ttk.Combobox(atk, width=15, height=20, state='readonly')
    CityList['value'] = ('서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기',
                         '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종')
    CityList.pack()
    CityList.place(x=180,y=115)
    CityList.current(0)
    TempFont = font.Font(atk, size=15, weight='bold', family='Consolas')
    CityText = Label(atk, text = '도시 선택', font=TempFont,bg="white")
    CityText.pack()
    CityText.place(x=40,y=110)

def InitAllSearchButton():
    TempFont = font.Font(atk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(atk, font = TempFont, text="검색",  command=AllSearchButtonAction,bg="white")
    SearchButton.place(x=390, y=110)

def AllSearchButtonAction():
    AllRenderText.configure(state='normal')
    AllRenderText.delete(0.0, END)

    AllSearchPlace()

    AllRenderText.configure(state='disabled')

def AllSearchPlace():
    trans_place = urllib.parse.quote_plus(CityList.get())
    key = spam.getkey()
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
    atk = Toplevel(gui)
    atk.geometry("650x700")
    photo = PhotoImage(file="cloud.gif")
    imageLabel = Label(atk, image=photo)
    imageLabel.pack()
    TempFont = font.Font(atk, size=20, weight='bold', family='Consolas')
    TopText = Label(atk, font=TempFont, text="[시도별 전체 지역 검색]",bg="white")
    TopText.place(x=60)

    InitAllSearchListBox()
    InitAllSearchButton()
    InitAllRenderText()
    EmailAddress2()
    atk.mainloop()

def SendEmail():
    text = RenderText.get("1.0", END)

    gmail_user = "yjm9494@gmail.com"
    gmail_pw = 'wlsaud94'

    to_addr = emailaddress.get()

    msg = MIMEMultipart('alternative')
    msg['From'] = gmail_user
    msg['To'] = to_addr
    msg['Subject'] = '대기정보'  # 제목
    msg.attach(MIMEText(text, 'plain', 'utf-8'))  # 내용 인코딩

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pw)
        server.sendmail(gmail_user, to_addr, msg.as_string())
        server.quit()
        print('success sent mail')

    except BaseException as e:
        print("failed send mail", str(e))

def EmailAddress():
    global emailaddress
    addressfont = font.Font(ptk, size=10, weight='bold', family='Consolas')
    PlaceText = Label(ptk, font=addressfont, text='보낼 이메일 주소',bg="white")
    PlaceText.place(x=40, y=820)
    TempFont = font.Font(ptk, size=13, weight='bold', family = 'Consolas')
    emailaddress = Entry(ptk, font = TempFont, width = 20, borderwidth = 12, relief = 'ridge')
    emailaddress.place(x=200, y=800)
    TempFont = font.Font(ptk, size=11, weight='bold', family='Consolas')
    SendButton = Button(ptk, font=TempFont, text="보내기", command=SendEmail,bg="yellow")
    SendButton.place(x=480, y=810)

def AllSendEmail():
    text = AllRenderText.get("1.0", END)

    gmail_user = "yjm9494@gmail.com"
    gmail_pw = 'wlsaud94'

    to_addr = emailaddress2.get()

    msg = MIMEMultipart('alternative')
    msg['From'] = gmail_user
    msg['To'] = to_addr
    msg['Subject'] = '대기정보'  # 제목
    msg.attach(MIMEText(text, 'plain', 'utf-8'))  # 내용 인코딩

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pw)
        server.sendmail(gmail_user, to_addr, msg.as_string())
        server.quit()
        print('success sent mail')

    except BaseException as e:
        print("failed send mail", str(e))

def EmailAddress2():
    global emailaddress2
    addressfont = font.Font(atk, size=10, weight='bold', family='Consolas')
    PlaceText = Label(atk, font=addressfont, text='보낼 이메일 주소',bg="white")
    PlaceText.place(x=40, y=620)
    TempFont = font.Font(atk, size=13, weight='bold', family = 'Consolas')
    emailaddress2 = Entry(atk, font = TempFont, width = 20, borderwidth = 12, relief = 'ridge')
    emailaddress2.place(x=200, y=600)
    TempFont = font.Font(atk, size=11, weight='bold', family='Consolas')
    SendButton = Button(atk, font=TempFont, text="보내기", command=AllSendEmail,bg="yellow")
    SendButton.place(x=480, y=610)

#지도
def InitMapButton():
    TempFont = font.Font(gui, size=12, weight='bold', family='Consolas')
    M_Button = Button(gui, font=TempFont, text="지역별 미세먼지 정보", command=MapButtonAction, width=20, height=2,bg="white")
    M_Button.pack()
    M_Button.place(x=170, y=400)

def MapButtonAction():
    global mtk
    mtk = Toplevel(gui)
    mtk.geometry("520x600")
    TempFont = font.Font(mtk, size=20, weight='bold', family='Consolas')
    TopText = Label(mtk, font=TempFont, text="[지역별 미세먼지 정보]",bg="white")
    TopText.place(x=60)

    photo = PhotoImage(file="map.gif")
    imageLabel = Label(mtk, image=photo)
    imageLabel.pack()
    imageLabel.place(x=50, y = 70)

    city = ['서울', '인천', '세종', '경기', '강원', '충남', '경북', '충북',
                         '대구', '대전', '전북', '광주', '경남', '울산', '부산', '전남', '제주']

    state = []
    color = []

    for i in range(17):
        pm10 = 0
        trans_place = urllib.parse.quote_plus(city[i])
        key = spam.getkey()
        url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey' + key + trans_place + '&ver=1.3'
        data = urllib.request.urlopen(url).read()
        root = ElementTree.fromstring(data)

        for child in root.iter('item'):
            if child.find('pm10Value').text == '-':
                pm10 = 0
            else:
                pm10 = int(child.find('pm10Value').text)
            break

        if pm10 < 30:
            state.append("좋음")
            color.append("blue")
        elif pm10 < 80:
            state.append("보통")
            color.append("green")
        elif pm10 < 150:
            state.append("나쁨")
            color.append("orange")
        if pm10 > 150:
            state.append("매우나쁨")
            color.append("red")

    seoul = Label(mtk, text=state[0], bg=color[0], fg="white", font="15")
    seoul.place(x=165, y=110)

    incheon = Label(mtk, text=state[1],bg=color[1],fg="white",font="15")
    incheon.place(x=112,y=135)

    saejong = Label(mtk, text=state[2],bg=color[2],fg="white",font="15")
    saejong.place(x=184,y=203)

    gyeonggi = Label(mtk, text=state[3], bg=color[3], fg="white", font="15")
    gyeonggi.place(x=210, y=148)

    gangwon = Label(mtk, text=state[4], bg=color[4], fg="white", font="15")
    gangwon.place(x=275, y=111)

    chungnam = Label(mtk, text=state[5], bg=color[5], fg="white", font="15")
    chungnam.place(x=130, y=231)

    gyengbook = Label(mtk, text=state[6], bg=color[6], fg="white", font="15")
    gyengbook.place(x=330, y=207)

    chungbuk = Label(mtk, text=state[7], bg=color[7], fg="white", font="15")
    chungbuk.place(x=260, y=194)

    daegoo = Label(mtk, text=state[8], bg=color[8], fg="white", font="15")
    daegoo.place(x=295, y=258)

    daegeon = Label(mtk, text=state[9], bg=color[9], fg="white", font="15")
    daegeon.place(x=230, y=254)

    jeonbuk = Label(mtk, text=state[10], bg=color[10], fg="white", font="15")
    jeonbuk.place(x=185, y=294)

    gwangju = Label(mtk, text=state[11], bg=color[11], fg="white", font="15")
    gwangju.place(x=135, y=324)

    gyengnam = Label(mtk, text=state[12], bg=color[12], fg="white", font="15")
    gyengnam.place(x=260, y=324)

    ulsan = Label(mtk, text=state[13], bg=color[13], fg="white", font="15")
    ulsan.place(x=352, y=298)

    busan = Label(mtk, text=state[14], bg=color[14], fg="white", font="15")
    busan.place(x=322, y=358)

    jeonnam = Label(mtk, text=state[15], bg=color[15], fg="white", font="15")
    jeonnam.place(x=175, y=380)

    jeju = Label(mtk, text=state[16], bg=color[16], fg="white", font="15")
    jeju.place(x=85, y=425)

    blue = Label(mtk, text="                ", bg="blue",font="5")
    blue.place(x=0, y=510)
    green = Label(mtk, text="                ", bg="green",font="5")
    green.place(x=125, y=510)
    orange = Label(mtk, text="                ", bg="orange", font="5")
    orange.place(x=248, y=510)
    red = Label(mtk, text="                ", bg="red", font="5")
    red.place(x=372, y=510)

    good = Label(mtk, text="좋음0    ~30", bg="white",fg="blue", font="12")
    good.place(x=0, y=535)
    normal = Label(mtk, text="보통     ~80", bg="white",fg="green", font="12")
    normal.place(x=125, y=535)
    bad = Label(mtk, text="나쁨    ~150", bg="white",fg="orange", font="12")
    bad.place(x=248, y=535)
    craze = Label(mtk, text="매우나쁨151~", bg="white",fg="red", font="12")
    craze.place(x=372, y=535)


    mtk.mainloop()



InitTopText()
InitDetailPlaceButton()
InitAllPlaceButton()
InitMapButton()

gui.mainloop()