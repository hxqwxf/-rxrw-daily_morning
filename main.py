from datetime import datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
from borax.calendars.festivals import LunarSchema


today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta =today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday(m,d):
  ls=LunarSchema(month=m,day=d)
  return ls.countdown()

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

ba=get_birthday(11,1)
ma=get_birthday(12,14)
me=get_birthday(12,2)
ge=get_birthday(3,18)
jie=get_birthday(5,12)
rui=get_birthday(10,4)
dujuan=get_birthday(6,5)
zw=get_birthday(10,22)
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"city":{"value":city},"temperature":{"value":temperature},"love_days":{"value":get_count()},"ba":{"value":ba},"ma":{"value":ma},"me":{"value":me},"ge":{"value":ge},"jie":{"value":jie},"rui":{"value":rui},"dujuan":{"value":dujuan},"zw":{"value":zw},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
