# -*- coding: utf-8 -*-
import scrapy
import csv
import os
import re
from ..items import FangjiaItem

class fangjiaSpider(scrapy.Spider):
    name = "fangjia"
    allowed_domins = ["https://xa.anjuke.com"]
    start_urls = []
    handle_httpstatus_list = [404,500]
    houseprice = [50,60,70,80]

    def after_404(self, response):
        print response.url
    def start_requests(self):
        global headers
        urlhead = 'https://xa.anjuke.com/sale/'
        for i_price in self.houseprice:
            housecondition = '?from_area=70&to_area=100&from_price=%s&to_price=100' %i_price
            for i in range(10):
               url = urlhead+'o4-p%s-t93-y2/%s#filtersort' %(i,housecondition) #按价格，从低到高，10年以后，12层以上，二手房,房屋总价50万起步
               self.start_urls.append(url)
        print self.start_urls       
        for url in self.start_urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        if response.status in self.handle_httpstatus_list:
             print 'wrong page'
        else:     
            fang_links = response.xpath('//ul[@id="houselist-mod-new"]/li[@class="list-item"]/div[@class="house-details"]/div/a/@href').extract()    
            if fang_links:
                for fang_link in fang_links:
                    url = fang_link
                    yield scrapy.Request(url,callback=self.parse_fangjia)

    def parse_fangjia(self, response):   # /是在根节点找(只找根节点下面一层,绝对) //是在根节点下面的所有节点找,相对
        info = []
        info_end = []
        item = FangjiaItem()
        broker_name = response.xpath('//p[@class="brokerInfo"]/text()').extract()[0]
        broker_tel  = response.xpath('//p[@class="brokerInfo"]/span[@class="mobile"]/text()').extract()[0]
        broker_tel.strip().strip('\t').strip('\n')
        broker_name.strip().strip('\t').strip('\n')

        name = response.xpath('//div[@class="houseInfoBox"]/div/div/div/div[@class="first-col detail-col"]/dl/dd/a/text()').extract()[0]
        location = response.xpath('//div[@class="houseInfoBox"]/div/div/div/div[@class="first-col detail-col"]/dl/dd/p/a/text()')
        location1 = location.extract()[0]
        location2 = location.extract()[1]
        detail = response.xpath('//div[@class="houseInfoBox"]/div/div/div/div[@class="first-col detail-col"]/dl/dd/p/text()')
        year = response.xpath('//div[@class="houseInfoBox"]/div/div/div/div[@class="first-col detail-col"]/dl/dd/text()').extract()[5]
        location3 = detail.extract()[1]
        address = location1 +'-'+ location2 + location3

        style = response.xpath('//div[@class="houseInfoBox"]/div/div/div/div[@class="second-col detail-col"]/dl/dd/text()')
        housestyle = style.extract()[0]
        housearea = style.extract()[1]
        height = style.extract()[3]


        houseinfo = response.xpath('//div[@class="houseInfoBox"]/div/div/div/div[@class="third-col detail-col"]/dl/dd/text()')
        decration = houseinfo.extract()[0]
        houseprice = houseinfo.extract()[1]
        firstpay = houseinfo.extract()[2]

        info.append(address)
        info.append(height)
        info.append(name)
        info.append(houseprice)
        info.append(housestyle)
        info.append(year)
        info.append(housearea)
        info.append(decration)
        info.append(firstpay)
        info.append(broker_name)
        info.append(broker_tel)

        filters_tab = ['灞桥'.decode('utf-8'),\
                        '经开区'.decode('utf-8'),\
                        '浐灞'.decode('utf-8'),\
                        '西咸新区'.decode('utf-8'),\
                        '高陵'.decode('utf-8'),\
                        '鄠邑'.decode('utf-8'),\
                        '临潼'.decode('utf-8'),\
                        '蓝田'.decode('utf-8'),\
                        '阎良'.decode('utf-8'),\
                        '周至'.decode('utf-8'),\
                        '西安周边'.decode('utf-8')]
        flag = 0
        for  filter_it in filters_tab:
            if filter_it in info[0]:
                flag = 1
        if  not flag:
            for i_info in info:
                i_info = i_info.decode('utf-8')
                if ' ' in i_info:
                    str1 = re.sub(' ','',i_info)
                    i_info = str1
                if  '\n' in  i_info:
                    str2 = re.sub('\n','',i_info)
                    i_info = str2
                if   '\t' in i_info:
                    str3 = re.sub('\t','',i_info)
                    i_info = str3
                info_end.append(i_info)
                print i_info
        else:
            pass
        if len(info_end) > 0 :
            item['FANGJIA_ADDRESS'] = info_end[0]
            item['FANGJIA_HEIGHIT'] = info_end[1]
            item['FANGJIA_NAME'] = info_end[2]
            item['FANGJIA_PRICE'] = info_end[3]
            item['FANGJIA_HOUSESTYLE'] = info_end[4]
            item['FANGJIA_BUILDTIME'] = info_end[5]
            item['FANGJIA_AREA'] = info_end[6]
            item['FANGJIA_DECORATION'] = info_end[7]
            item['FANGJIA_FIRSTPAY'] = info_end[8]
            item['FANGJIA_BROKERNAME'] = info_end[9]
            item['FANGJIA_BROKERTEL'] = info_end[10]
        yield item
