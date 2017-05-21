__author__ = 'WarmingWang'
# -*- coding: UTF-8 -*-

from urllib.request import urlopen
import json 
import baselib



class WEATHER:

    def __init__(self, citykey, day):
        self.citykey = citykey	#上海101020100 杭州101210101
        self.day = day			#今天天气 [-1,4]
        self.weatherInfo = {}

    def getWeatherInfo(self):
        weatherUrl = 'http://wthrcdn.etouch.cn/weather_mini?citykey=' + self.citykey 
        jsonStr = urlopen(weatherUrl).read()
        base = baselib.BASE()
        jsonStr = base.ungzip(jsonStr)
        data = json.loads(jsonStr.decode('utf-8'))
        weather = data['data']
        #self.weatherInfo{'aqi':weather['aqi']}
        self.weatherInfo = {'aqi' : weather['aqi'],'currTemp' : weather['wendu'], 'city' : weather['city'], 'tips' : weather['ganmao'],      \
                         'highTemp' : weather['forecast'][self.day]['high'], 'lowTemp' : weather['forecast'][self.day]['low'],            \
                         'weatherType' : weather['forecast'][self.day]['type'], 'fengxiang' : weather['forecast'][self.day]['fengxiang'], \
                         'fengli' : weather['forecast'][self.day]['fengli']}

       # return (aqi, currTemp, city, tips, highTemp, lowTemp, weatherType, fengxiang, fengli)
