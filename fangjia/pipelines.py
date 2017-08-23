# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv,datetime
import sys
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')

class FangjiaPipeline(object):
    def process_item(self, item, spider):
        return item
class Csv_writer_Pipeline(object):
    time_stamp = "%Y_%m_%d_%H_%M_%S"
    content = ['FANGJIA_ADDRESS',\
    'FANGJIA_HEIGHIT',\
    'FANGJIA_NAME',\
    'FANGJIA_PRICE',\
    'FANGJIA_HOUSESTYLE',\
    'FANGJIA_BUILDTIME',\
    'FANGJIA_AREA',\
    'FANGJIA_DECORATION',\
    'FANGJIA_FIRSTPAY',\
    'FANGJIA_BROKERNAME',\
    'FANGJIA_BROKERTEL']
    def __init__(self):
        self.filename = 'ershoufang_{0}.csv'.format(datetime.datetime.now().strftime(self.time_stamp))
        self.file_obj = open(self.filename,'ab')
        self.file_obj.write(codecs.BOM_UTF8)
        self.writer = csv.writer(self.file_obj)
        self.writer.writerow([' ',\
            '地址',\
            '楼层高度',\
            '楼盘名称',\
            '房屋价格',\
            '房屋样式',\
            '建造年代',\
            '面积',\
            '装修程度',\
            '首付(30%)',\
            '房屋经纪人',\
            '经纪人联系方式'])

    def process_item(self, item, spider):
        self.writer.writerow([' ',\
            item[self.content[0]],\
            item[self.content[1]],\
            item[self.content[2]],\
            item[self.content[3]],\
            item[self.content[4]],\
            item[self.content[5]],\
            item[self.content[6]],\
            item[self.content[7]],\
            item[self.content[8]],\
            item[self.content[9]],\
            item[self.content[10]]])
        return item