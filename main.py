from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random


today = datetime.now()
week_day = {
    0: '星期一',
    1: '星期二',
    2: '星期三',
    3: '星期四',
    4: '星期五',
    5: '星期六',
    6: '星期日',
}
today_weekday = week_day[today.weekday()]
current_date = str(today.date()) + " " + today_weekday


start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"].split(",")
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['low']), math.floor(weather['high'])


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


#
# def get_birthday():
#     next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
#     if next < datetime.now():
#         next = next.replace(year=next.year + 1)
#     return (next - today).days


def get_words():
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return {"ch": note, "en": content}


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, min_temperature, max_temperature = get_weather()
words = get_words()
data = {"date": {"value": current_date, "color": get_random_color()},
        "weather": {"value": wea, "color": get_random_color()},
        "min_temperature": {"value": min_temperature, "color": get_random_color()},
        "max_temperature": {"value": max_temperature, "color": get_random_color()},
        "love_days": {"value": get_count(), "color": get_random_color()},
        "en": {"value": words['en'], "color": get_random_color()},
        "ch": {"value": words['ch'], "color": get_random_color()}, "city": {"value": city, "color": get_random_color()}}
for user in user_id:
    print("用户弟弟弟弟： " + user)
    res = wm.send_template(user, template_id, data)
print(res)
