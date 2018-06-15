import telepot
import sys
import time
import sqlite3
import telepot
import urllib.parse
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback
import noti


def replyAptData(loc_param, user, ver='1.3'):
    print(user, loc_param, ver)
    trans = urllib.parse.quote_plus(loc_param)
    res_list = noti.getData(trans, ver)
    msg = ''

    for r in res_list:
        print(str(datetime.now()).split('.')[0], r)
        if len(r + msg) + 1 > noti.MAX_MSG_LENGTH:
            noti.sendMessage(user, msg)
            msg = r + '\n'
        else:
            msg += r + '\n'
    if msg:
        noti.sendMessage(user, msg)
    else:
        noti.sendMessage(user, '%s은 관측할 수 없는 지역입니다.' % loc_param)


def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        noti.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage( user, row )


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')
    if text.startswith('지역') and len(args)>1:
        print('try to 지역', args[1])
        replyAptData(args[1], chat_id, '1.3')
    elif text.startswith('버전') and len(args)>1:
        print('try to 버전', args[1])
        replyAptData(args[1], chat_id, '1.3' )
#    elif text.startswith('저장')and len(args)>1:
#        print('try to 저장', args[1])
#        save(chat_id, args[1])
#    elif text.startswith('확인'):
#        print('try to 확인')
#        check(chat_id)
    else:
        noti.sendMessage(chat_id, """모르는 명령어입니다.
        \날씨 [YYYYMM] [지역번호] \n지역 [지역번호] \n저장 [지역번호] 
        \n확인 중 하나의 명령을 입력하세요.\n     지역 ["서울",
         "부산", "대구", "인천", "광주",
          "대전", "울산", "경기", "강원", 
              "충북", "충남", "전북", "전남",
               "경북", "경남", "제주", "세종",
               """)

today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', noti.TOKEN )

bot = telepot.Bot(noti.TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)


#def handle(msg):
#    pass

#url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey=u6gWf4hX%2FqPazPKbDjPWntYuufDTcONxlxtmymo%2F3VhDV92yP41s7dJYuiCKwODnvOflyT8MRLXKcmlgmTz9ww%3D%3D&numOfRows=10&pageSize=10&pageNo=1&startPage=1&sidoName=%EC%84%9C%EC%9A%B8&ver=1.3'

#bot = telepot.Bot('612655230:AAEzms-YNzrEFiHHs2iHfslpIHE0TouMwOc')
#bot.getMe()
#bot.sendMessage('533391619', '안녕하세요 원주연 입니다. 텀프 하고있습니다~')