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
    soup = BeautifulSoup(res_body, 'html.parser')
    items = soup.findAll('item')
    for item in items:
        item = re.sub('<.*?>', '|', item.text)
        if (n%2 == 0):
            parsed = item.split('|')
        try:
            print(parsed[0])
            print('======================================================================')
            row = '지역 : ' + parsed[0] #+ '(' + parsed[1] + ')' + '시간 : ' + parsed[2] + '산소 농도 : ' + parsed[3] + '일산화탄소 농도 : ' + parsed[4] + '오존 농도 : ' + parsed[5] +'이산화질소 농도 : ' + parsed[6] + '미세먼지 농도 : ' + parsed[7] + '㎍/㎥' + '초미세먼지 농도 : ' + parsed[8] + '㎍/㎥'
        except IndexError:
            row = item.replace('|', ',')

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


if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)