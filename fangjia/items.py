# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangjiaItem(scrapy.Item):
    # define the fields for your item here like:
    FANGJIA_ADDRESS = scrapy.Field()  # 住房地址
    FANGJIA_HEIGHIT = scrapy.Field()  #楼层高度
    FANGJIA_NAME = scrapy.Field()     # 名字
    FANGJIA_PRICE = scrapy.Field()    # 房价
    FANGJIA_HOUSESTYLE =  scrapy.Field() #房屋样子
    FANGJIA_BUILDTIME = scrapy.Field() # 建造年代
    FANGJIA_AREA = scrapy.Field()     # 住房面积
    FANGJIA_DECORATION = scrapy.Field() #装修程度
    FANGJIA_FIRSTPAY = scrapy.Field() #首付
    FANGJIA_BROKERNAME = scrapy.Field()  # 经纪人名字
    FANGJIA_BROKERTEL = scrapy.Field()   #经纪人电话
