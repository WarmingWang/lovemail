__author__ = 'WarmingWang'
# -*- coding: UTF-8 -*-

from urllib.request import urlopen
import re

class FORTUNE:
	
    def __init__(self, constellation):
        self.constellation = constellation
        self.fortune1 = []
        self.fortune2 = []
        self.fortune3 = []

    def getFortune1(self, data):
        cer = re.compile('</label><span class="star_m star_blue"><em style="width:(.*?)px', flags=0)
        strlist = cer.findall(data)
        #print (strlist[0],strlist[1])
        return strlist
    
    def getFortune2(self, data):
        cer = re.compile('健康指数：(.*?)</li></ul></dd>', flags=0)
        strlist = cer.findall(data)
        return strlist
    
    def getFortune3(self, data):
        cer = re.compile('<div class="c_cont">[\s\S]*?<p>(.*)</p>', flags=0)
        strlist = cer.findall(data)
        #print (strlist)
        return strlist
        
    def getFortuneInfo(self):
        fortuneUrl = 'http://www.xzw.com/fortune/' + self.constellation 
        fortuneHtml = urlopen(fortuneUrl).read().decode('gb2312')
        self.fortune1 = self.getFortune1(fortuneHtml)
        self.fortune2 = self.getFortune2(fortuneHtml)
        self.fortune3 = self.getFortune3(fortuneHtml)
        print ('get fortune success...')
