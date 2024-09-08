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
msg1=''
# 处理每一行数据
student_list = []
advanced=[]
for student in students:
    name, birth,month,day,countdown = student.strip().split(',')  # 去除行尾空白并按逗号分割字段
    student_list.append({'name': name, 'birth': birth, 'month': month,'day':day,'countdown': countdown})

# 计算生日
for student in student_list:
    ls=LunarSchema(month=int(student['month']),day=int(student['day']))
    student['countdown']=ls.countdown()
    text='距离{}生日{}还有:{}天\n'.format(student['name'],student['birth'],student['countdown'])
    msg+=text
    if(student['countdown']<=30):
        advanced.append(student)
        
# 倒计时小于30天的提醒
for student in advanced:
    text1='距离{}生日{}还有:{}天\n'.format(student['name'],student['birth'],student['countdown'])
    msg1+=text1
if(len(msg1)==0):
    msg1='目前还没有哦~'
    
def get_count():
    delta =today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code!=200:
        return get_words()
    return words.json()['data']['text']

data = {
    'msg': '生日推送@face=53@ \n------\n今日日期：{}\n今天是我来到世界的:{}天\n------\n'.format(date,get_count())+msg+'每日一言\n{}'.format(get_words())
}

data1={
    'msg':'生日倒计时小于30天提醒\n------\n'+msg1
}
res=requests.post(webhook, data)
print(res)
time.sleep(10)
res1=requests.post(webhook, data1)
print(res1)
