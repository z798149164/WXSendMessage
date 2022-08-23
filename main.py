from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random


# text = requests.get("https://api.oddfar.com/yl/q.php?c=2011&encode=text").text

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

user_id = os.environ["USER_ID"]
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
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, min_temperature, max_temperature = get_weather()
data = {"date": {"value": current_date, "color": get_random_color()}, "weather": {"value": wea, "color": get_random_color()},
        "min_temperature": {"value": min_temperature, "color": get_random_color()}, "max_temperature": {"value": max_temperature, "color": get_random_color()},
        "love_days": {"value": get_count(), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()}, "city": {"value": city, "color": get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
