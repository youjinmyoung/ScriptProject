from tkinter import *
from tkinter import font
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
    global SearchListBox
    SearchFont = font.Font(gui, size=15, weight='bold', family='Consolas')
    l2 = Label(gui, font=SearchFont, text='도시 선택')
    l2.place(x=40, y=105)
    ListBoxScrollbar = Scrollbar(gui)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x = 350, y=50)

    TempFont = font.Font(gui, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(gui, font=TempFont, activestyle='none',
                            width = 10, height = 4, borderwidth = 12, relief = 'ridge',
                            yscrollcommand = ListBoxScrollbar.set)

    SearchListBox.insert(1, "서울")
    SearchListBox.insert(2, "부산")
    SearchListBox.insert(3, "대구")
    SearchListBox.insert(4, "인천")
    SearchListBox.insert(5, "광주")
    SearchListBox.insert(6, "대전")
    SearchListBox.insert(7, "울산")
    SearchListBox.insert(8, "경기")
    SearchListBox.insert(9, "강원")
    SearchListBox.insert(11, "충북")
    SearchListBox.insert(12, "충남")
    SearchListBox.insert(13, "전북")
    SearchListBox.insert(14, "전남")
    SearchListBox.insert(15, "경북")
    SearchListBox.insert(16, "경남")
    SearchListBox.insert(17, "제주")
    SearchListBox.insert(18, "세종")

    SearchListBox.pack()
    SearchListBox.place(x=180, y=50)
    ListBoxScrollbar.config(command=SearchListBox.yview)


def InitInputLabel():
    global InputLabel
    SearchFont = font.Font(gui, size=15, weight='bold', family='Consolas')
    l1 = Label(gui, font=SearchFont, text='지역 이름')
    l1.place(x=40, y=245)
    TempFont = font.Font(gui, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(gui, font = TempFont, width = 12, borderwidth = 12, relief = 'ridge')
    InputLabel.place(x=180, y=230)

def InitSearchButton():
    TempFont = font.Font(gui, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(gui, font = TempFont, text="검색",  command=SearchButtonAction)
    SearchButton.place(x=390, y=240)

def SearchButtonAction():
    global SearchListBox

    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    SearchPlace()

    RenderText.configure(state='disabled')

def SearchPlace():
    trans_place = urllib.parse.quote_plus(InputLabel.get())
    key = '=u6gWf4hX%2FqPazPKbDjPWntYuufDTcONxlxtmymo%2F3VhDV92yP41s7dJYuiCKwODnvOflyT8MRLXKcmlgmTz9ww%3D%3D&numOfRows=40&pageSize=10&pageNo=1&startPage=1&sidoName='
    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey' + key + trans_place + '&ver=1.3'
    data = urllib.request.urlopen(url).read()
    root = ElementTree.fromstring(data)

    for child in root.iter('item'):
        time = child.find('dataTime').text
        name = child.find('stationName').text
        so2 = child.find('so2Value').text
        co = child.find('coValue').text
        o3 = child.find('o3Value').text
        no2 = child.find('no2Value').text
        RenderText.insert(INSERT,'시간 : ' + time)
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT,'지역 : ' + name + '\nSo2 측정량 : ' + so2 +
                '\nCo 측정량 : ' + co + '\nO3 측정량 : ' + o3 + '\nNo2 측정량 : ' + no2)
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, '=================================================')
        RenderText.insert(INSERT, "\n")

def InitRenderText():
    global RenderText
    RenderTextScrollbar = Scrollbar(gui)
    RenderText = Text(gui, width=50, height=27, borderwidth=12,
                      relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=40, y=300)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side = RIGHT, fill = BOTH)


    RenderText.configure(state='disabled')


InitTopText()
InitSearchListBox()
InitInputLabel()
InitSearchButton()
InitRenderText()
gui.mainloop()