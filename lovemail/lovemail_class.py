__author__ = 'WarmingWang'
# -*- coding: UTF-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from urllib.request import urlopen
import smtplib
import os
import sys
import loveMovieScreenshots
import htmlTXT
import datetime

class SENDEMAIL:
    #get pic about love movies
    d_1stWeMeet = datetime.date(2017, 4, 2)		#the first time we meet
    now = datetime.datetime.now().date()
    days = (now - d_1stWeMeet).days
    num = days - 307 * int(days / 307)      #循环取0-306张图
    picUrl = 'https://www.douban.com/photos/album/157693223/?start=' + str(num)
    picHtml = urlopen(picUrl).read().decode('utf-8')
    screenShot = loveMovieScreenshots.LMSS()
    picAbsFilename = screenShot.picAbsFilename
    imageAddr = 'https://img3.doubanio.com/view/photo/large/public/p' + screenShot.getImageAddr(picHtml) +'.jpg'
    screenShot.saveImg(imageAddr)
    
    
    def __init__(self, to_addr):
        self.from_addr = 'youraccount@gmail.com'
        self.password = 'password'
        self.to_addr = [to_addr]#'XXX@qq.com'
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        
    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def sendemail(self):
        message = MIMEMultipart()
        message['From'] = self._format_addr('王小明 <%s>' % self.from_addr)
        message['To'] = self._format_addr('小明 <%s>' % self.to_addr)
        message['Subject'] = Header('Greetings from WarmingWang...', 'utf-8').encode()

        htmlTxt = htmlTXT.htmlTxt
        msg = MIMEText(htmlTxt, 'html', 'utf-8')
        
        #添加照片附件
        with open(self.picAbsFilename,'rb')as fp:
            picture = MIMEImage(fp.read())
            picture['Content-Type'] = 'application/octet-stream'
            picture['Content-Disposition'] = 'attachment;filename=' + self.picAbsFilename
            picture['Content-ID'] = '<0>'
        
        #将内容附加到邮件主体中
        message.attach(msg)
        message.attach(picture)

        while 1:
            try:
                server = smtplib.SMTP()
                server.connect(self.smtp_server, self.smtp_port)
                server.starttls()
                #server.set_debuglevel(1)
                server.login(self.from_addr, self.password)
                server.sendmail(self.from_addr, self.to_addr, message.as_string())
                server.quit()
                print ("send email to %s success..." % (self.to_addr))
                break
            except smtplib.SMTPException as e:
                print ('send email error...', e)

if __name__ == "__main__":
    send = SENDEMAIL('heraccount@qq.com')
    send.sendemail()
