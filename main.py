from datetime import datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
from borax.calendars.festivals import LunarSchema
key=os.environ['QMSG_KEY']
webhook = 'https://qmsg.zendee.cn/send/'+key   # Qmsg酱接口
today = datetime.now()
date=today.strftime('%Y-%m-%d')
start_date = os.environ['START_DATE']


# 打开文件并读取内容
with open('birthday.txt', 'r', encoding='utf-8') as file:
    students = file.readlines()  # 读取所有行
msg=''
# 处理每一行数据
student_list = []
for student in students:
    name, birth,month,day,countdown = student.strip().split(',')  # 去除行尾空白并按逗号分割字段
    student_list.append({'name': name, 'birth': birth, 'month': month,'day':day,'countdown': countdown})

# 计算生日
for student in student_list:
    ls=LunarSchema(month=int(student['month']),day=int(student['day']))
    student['countdown']=ls.countdown()
    text='距离{}生日{}还有:{}天\n'.format(student['name'],student['birth'],student['countdown'])
    msg+=text

def get_count():
    delta =today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code!=200:
        return get_words()
    return words.json()['data']['text']

data = {
    'msg': '生日推送@face=53@ \n------\n今日日期：{}\n今天是我来到世界的:{}天\n------\n'.format(date,get_count())+msg
}
res=requests.post(webhook, data)
print(res)
print(data)
