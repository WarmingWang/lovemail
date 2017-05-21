__author__ = 'WarmingWang'
# -*- coding: UTF-8 -*-

import weather
import fortune


#get fortune about pisces
constellation = {'白羊':'aries',      '金牛':'taurus',   '双子':'gemini',  '巨蟹':'cancer', \
                 '狮子':'leo',        '处女':'virgo',    '天秤':'libra',   '天蝎':'scorpio',\
                 '射手':'sagittarius','摩羯':'capricorn','水瓶':'aquarius','双鱼':'pisces'}
fortune = fortune.FORTUNE(constellation['天秤'])
fortune.getFortuneInfo()

#get weatherinfo 
citykey = '101210101'        #星座和城市信息应从数据库里取出
day = 0
weather = weather.WEATHER(citykey, day)
weather.getWeatherInfo()
city = weather.weatherInfo['city']
aqi = weather.weatherInfo['aqi']
currTemp = weather.weatherInfo['currTemp']
highTemp = weather.weatherInfo['highTemp']
lowTemp = weather.weatherInfo['lowTemp']
weatherType = weather.weatherInfo['weatherType']
fengxiang = weather.weatherInfo['fengxiang']
fengli = weather.weatherInfo['fengli']
tips = weather.weatherInfo['tips']

htmlTxt = '''<html><body>
    <h3>Dear, 小明：</h3>
    <hr>
    <div style="text-indent:2em">
    <p>今天'''+ city +'''当前温度'''+ currTemp +'''度，最'''+ highTemp +'''，最'''+ lowTemp +'''，'''+ weatherType +'''，空气质量指数'''+ aqi +'''，风向'''+ fengxiang +'''，风力'''+ fengli +'''</p>
    <p>小小明提示：'''+ tips +'''</p>
    </div>
    <dl><dd><h4>天秤座今日运势</h4><ul><li><label>整体运势：</label>'''+ '*'*int(int(fortune.fortune1[0])/16) +'''</li><li><label>爱情运势：</label>'''+ '*'*int(int(fortune.fortune1[1])/16) +'''
    </li><li><label>事业学业：</label>'''+ '*'*int(int(fortune.fortune1[2])/16) +'''</li><li><label>财富运势：</label>'''+ '*'*int(int(fortune.fortune1[3])/16) +'''
    </li><li><label>健康指数：'''+ fortune.fortune2[0] +'''</li></ul></dd></dl>
    <div style="text-indent:2em">
    <p>'''+ fortune.fortune3[0] +'''</p>
    <p>I wish you have a nice day, and lucky around you the whole day.</p>
    </div>
    <br>
    <p style="text-align:right">Best Wishes, 王小明</p>
    <p><img src="cid:0"></p>
    </body></html>
    '''
#print (htmlTxt)
