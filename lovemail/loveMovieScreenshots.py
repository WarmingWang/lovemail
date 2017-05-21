__author__ = 'WarmingWang'
# -*- coding: UTF-8 -*-

from urllib.request import urlopen
import re
import os
import sys


class LMSS:
    
    fileCWD = os.path.dirname(os.path.abspath(sys.argv[0]))
    picName = '/love.jpg'
    picAbsFilename = fileCWD + picName

    def getImageAddr(self, data):
        cer = re.compile('https://www.douban.com/photos/photo/(.*?)/"', flags=0)
        strlist = cer.findall(data)
    #    print (strlist[0])
        return strlist[0]

    def saveImg(self, imageURL):
        op = urlopen(imageURL)
        data = op.read()
        f = open(self.picAbsFilename, 'wb')
        f.write(data)
        print ('save image success')
        f.close()


#url = 'https://www.douban.com/photos/album/157693223/?start=' + str(1)


#html = urlopen(url).read().decode('utf-8')

#imageAddr = 'https://img3.doubanio.com/view/photo/large/public/p' + getImageAddr(html) +'.jpg'

