__author__ = 'WarmingWang'
# -*- coding: UTF-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from urllib.request import urlopen
import re
import datetime
import gzip
import json
import smtplib
import os
import sys

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def ungzip(data):
    try:  # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data
    
def getImageAddr(data):
    cer = re.compile('https://www.douban.com/photos/photo/(.*?)/"', flags=0)
    strlist = cer.findall(data)
#    print (strlist)
    return strlist[0]

def saveImg(imageURL, fileName):
    op = urlopen(imageURL)
    data = op.read()
    f = open(fileName, 'wb')
    f.write(data)
    print ('save image success...')
    f.close()

#strlist
def getFortune1(data):
    cer = re.compile('</label><span class="star_m star_blue"><em style="width:(.*?)px', flags=0)
    strlist = cer.findall(data)
#    print (strlist[0],strlist[1])
    return strlist

def getFortune2(data):
    cer = re.compile('健康指数：(.*?)<li><label>速配星座.*?<li class="desc"><label>(.*?)</li></ul></dd>', flags=0)
    strlist = cer.findall(data)
#    print (strlist[0][0],strlist[0][1])
    return strlist

def getFortune3(data):
    cer = re.compile('<div class="c_cont">[\s\S]*?<p>(.*)</p>', flags=0)
    strlist = cer.findall(data)
#    print (strlist)
    return strlist

d_1stWeMeet = datetime.date(2017, 4, 2)		#the first time we meet
now = datetime.datetime.now().date()
days = (now - d_1stWeMeet).days
num = days - 307 * int(days / 307)		#循环取0-306张图
print ("From the first time we have met already %d days.\nPoint the pic %d." % (days, num))
fileCWD = os.path.dirname(os.path.abspath(sys.argv[0]))
picName = '/love.jpg'
picAbsFilename = fileCWD + picName
cityKey = '101020100'		#上海101020100 杭州101210101

#get pic about love movies
picUrl = 'https://www.douban.com/photos/album/157693223/?start=' + str(num)
picHtml = urlopen(picUrl).read().decode('utf-8')

imageAddr = 'https://img3.doubanio.com/view/photo/large/public/p' + getImageAddr(picHtml) +'.jpg'
saveImg(imageAddr, picAbsFilename)

#get fortune about pisces
fortuneUrl = 'http://www.xzw.com/fortune/pisces/'	#双鱼
fortuneHtml = urlopen(fortuneUrl).read().decode('gb2312')

fortune1 = getFortune1(fortuneHtml)
fortune2 = getFortune2(fortuneHtml)
fortune3 = getFortune3(fortuneHtml)
print ('get fortune success...')

#get weatherinfo
weatherUrl = 'http://wthrcdn.etouch.cn/weather_mini?citykey=' + cityKey	
jsonStr = urlopen(weatherUrl).read()
jsonStr = ungzip(jsonStr)
data = json.loads(jsonStr.decode('utf-8'))

weatherInfo = data['data']
#print (weatherInfo)
aqi = weatherInfo['aqi']
currTemp = weatherInfo['wendu']
city = weatherInfo['city']
tips = weatherInfo['ganmao']

forecastToday = weatherInfo['forecast'][0]
highTemp = forecastToday['high']
lowTemp = forecastToday['low']
weatherType = forecastToday['type']
fengxiang = forecastToday['fengxiang']
fengli = forecastToday['fengli']
print ('get weatherInfo success...')

#send emails
from_addr = 'youraccount@gmail.com'
password = 'password'
to_addr = ['heraccount@qq.com','XXX@qq.com']
smtp_server = 'smtp.gmail.com'
smtp_port = 587

message = MIMEMultipart()
message['From'] = _format_addr('王小明 <%s>' % from_addr)
message['To'] = _format_addr('小明 <%s>' % to_addr)
message['Subject'] = Header('Greetings from WarmingWang...', 'utf-8').encode()
htmlTxt = '''<html><body>
    <h3>Hello, 小明：</h3>
    <hr>
    <div style="text-indent:2em">
    <p>From the first time we have met already '''+ str(days) +''' days.</p>
    <p>今天'''+ city +'''当前温度'''+ currTemp +'''度，最'''+ highTemp +'''，最'''+ lowTemp +'''，'''+ weatherType +'''，空气质量指数'''+ aqi +'''，风向'''+ fengxiang +'''，风力'''+ fengli +'''</p>
    <p>小小明提示：'''+ tips +'''</p>
    </div>
    <dl><dd><h4>双鱼座今日运势</h4><ul><li><label>整体运势：</label>'''+ '*'*int(int(fortune1[0])/16) +'''</li><li><label>爱情运势：</label>'''+ '*'*int(int(fortune1[1])/16) +'''
    </li><li><label>事业学业：</label>'''+ '*'*int(int(fortune1[2])/16) +'''</li><li><label>财富运势：</label>'''+ '*'*int(int(fortune1[3])/16) +'''
    </li><li><label>健康指数：'''+ fortune2[0][0] +'''<li><label>速配星座：</label>天秤座</li><li><label>'''+ fortune2[0][1] +'''</li></ul></dd></dl>
    <div style="text-indent:2em">
    <p>'''+ fortune3[0] +'''</p>
    <p>I wish you have a nice day, and lucky around you the whole day.</p>
    </div>
    <br>
    <p style="text-align:right">Best Wishes, 王小明</p>
    <p><img src="cid:0"></p>
    </body></html>
    '''
print (htmlTxt)
msg = MIMEText(htmlTxt, 'html', 'utf-8')

#添加照片附件
with open(picAbsFilename,'rb')as fp:
    picture = MIMEImage(fp.read())
    picture['Content-Type'] = 'application/octet-stream'
    picture['Content-Disposition'] = 'attachment;filename=' + picAbsFilename
    picture['Content-ID'] = '<0>'

#将内容附加到邮件主体中
message.attach(msg)
message.attach(picture)

while 1:
    try:
        server = smtplib.SMTP()
        server.connect(smtp_server, smtp_port)
        server.starttls()
        #server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, message.as_string())
        server.quit()
        print ("send email to %s success..." % (to_addr))
        break
    except smtplib.SMTPException as e:
        print ('send email error...', e)
