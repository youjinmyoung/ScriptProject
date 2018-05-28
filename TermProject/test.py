from tkinter import *
from tkinter import font
from tkinter import ttk
import tkinter.messagebox
import urllib.request
import urllib.parse
from xml.etree import ElementTree

gui = Tk()
gui.geometry("570x800+750+200")

def InitTopText():
    TempFont = font.Font(gui, size=20, weight='bold', family='Consolas')
    MainText = Label(gui, font=TempFont, text="[전국 시도별 대기상태 검색 App]")
    MainText.place(x = 20)

def InitSearchListBox():
    global CityList
    CityList = ttk.Combobox(gui, width=15, height=20, state='readonly')
    CityList['value'] = ('서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기',
                         '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종')
    CityList.pack()
    CityList.place(x=180,y=75)
    CityList.current(0)
    TempFont = font.Font(gui, size=15, weight='bold', family='Consolas')
    CityText = Label(gui, text = '도시 선택', font=TempFont)
    CityText.pack()
    CityText.place(x=40,y=70)

def InitInputLabel():
    global InputLabel
    SearchFont = font.Font(gui, size=15, weight='bold', family='Consolas')
    PlaceText = Label(gui, font=SearchFont, text='지역 이름')
    PlaceText.place(x=40, y=150)
    TempFont = font.Font(gui, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(gui, font = TempFont, width = 12, borderwidth = 12, relief = 'ridge')
    InputLabel.place(x=180, y=140)

def InitSearchButton():
    TempFont = font.Font(gui, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(gui, font = TempFont, text="검색",  command=SearchButtonAction)
    SearchButton.place(x=390, y=150)

def SearchButtonAction():
    global SearchListBox

    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    SearchPlace()

    RenderText.configure(state='disabled')

def SearchPlace():
    flag = True
    trans_place = urllib.parse.quote_plus(CityList.get())
    key = '=u6gWf4hX%2FqPazPKbDjPWntYuufDTcONxlxtmymo%2F3VhDV92yP41s7dJYuiCKwODnvOflyT8MRLXKcmlgmTz9ww%3D%3D&numOfRows=40&pageSize=10&pageNo=1&startPage=1&sidoName='
    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey' + key + trans_place + '&ver=1.3'
    data = urllib.request.urlopen(url).read()
    root = ElementTree.fromstring(data)
    DataList = []
    SubList = []

    for child in root.iter('item'):
        p_name = child.find('stationName').text
        if InputLabel.get() == p_name:
            p_time = child.find('dataTime').text
            p_so2 = child.find('so2Value').text
            p_co = child.find('coValue').text
            p_o3 = child.find('o3Value').text
            p_no2 = child.find('no2Value').text
            flag = False
        if flag == False:
            break

    n =  '지역 : ' + p_name + '\nSo2 측정량 : ' + p_so2 + '\nCo 측정량 : ' + p_co + '\nO3 측정량 : ' + p_o3 + '\nNo2 측정량 : ' + p_no2

    print(n)

def InitRenderText():
    global RenderText
    RenderTextFrame = Frame(gui)
    RenderTextScrollbar = Scrollbar(RenderTextFrame)
    RenderTextScrollbar.pack(side='right', fill="y")
    RenderText = Text(RenderTextFrame, width=50, height=27, borderwidth=12,
                      relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderTextScrollbar.config(command=RenderText.yview)


    RenderText.pack()
    RenderTextFrame.pack()
    RenderTextFrame.place(x=40, y=210)



    RenderText.configure(state='disabled')


InitTopText()
InitSearchListBox()
InitInputLabel()
InitSearchButton()
InitRenderText()
gui.mainloop()