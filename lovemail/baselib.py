__author__ = 'WarmingWang'
# -*- coding: UTF-8 -*-

import gzip

class BASE:
	
    def ungzip(self, data):
        try:  # 尝试解压
            print('正在解压.....')
            data = gzip.decompress(data)
            print('解压完毕!')
        except:
            print('未经压缩, 无需解压')
        return data