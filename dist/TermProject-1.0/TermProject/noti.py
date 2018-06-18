import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
from datetime import date, datetime, timedelta
import traceback
from xml.etree import ElementTree


key = 'u6gWf4hX%2FqPazPKbDjPWntYuufDTcONxlxtmymo%2F3VhDV92yP41s7dJYuiCKwODnvOflyT8MRLXKcmlgmTz9ww%3D%3D&numOfRows=40&pageSize=40&pageNo=1&startPage=1'
TOKEN = '612655230:AAEzms-YNzrEFiHHs2iHfslpIHE0TouMwOc'
MAX_MSG_LENGTH = 300
baseurl = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey=' + key
bot = telepot.Bot(TOKEN)
n = 0

def getData(loc_param, ver):
    global n
    res_list = []
    url = baseurl + '&sidoName=' + loc_param + '&ver=' + ver
    res_body = urlopen(url).read()
    root = ElementTree.fromstring(res_body)
    for child in root.iter('item'):
        p_name = child.find('stationName').text
        p_time = child.find('dataTime').text
        p_so2 = child.find('so2Value').text
        p_co = child.find('coValue').text
        p_o3 = child.find('o3Value').text
        p_no2 = child.find('no2Value').text
        pm10 = child.find('pm10Value').text
        pm25 = child.find('pm25Value').text
        row = '시간 : ' + p_time + '\n지역 : ' + p_name + '\nSo2 측정량 : ' + p_so2 + '\nCo 측정량 : ' + p_co + \
              '\nO3 측정량 : ' + p_o3 + '\nNo2 측정량 : ' + p_no2 + '\n미세먼지 : ' + pm10 + '\n초미세먼지 : ' + pm25

        if row:
            res_list.append(row.strip())
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(loc_param, ver='1.3'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, loc_param, ver)
        res_list = getData(ver, loc_param)
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user, r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(loc_param.now()).split('.')[0], r)
                if len(r+msg)+1 > MAX_MSG_LENGTH:
                    sendMessage(user, msg)
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage(user, msg )
    conn.commit()
