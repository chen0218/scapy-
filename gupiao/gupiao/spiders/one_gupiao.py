# -*- coding: utf-8 -*-
import scrapy
from gupiao.items import GupiaoOneItem
import re


class OneGupiaoSpider(scrapy.Spider):
    name = "one_gupiao"
#   allowed_domains = ["gupiao.com"]
    start_urls = ['http://quote.eastmoney.com/stocklist.html']

    def parse(self, response):
        f = open('cc.txt','r',encoding='utf-8')
        all_data = f.readlines()
        url_list = []
        for line in all_data:
            test = re.findall(r'(\d{6})',line)
            a = str(test).replace("['",'')
            b = str(a).replace("']",'')
            url_list.append(b)
#        gupiao_id_list = [600438,600001,600033]

        url1 = 'http://mdfm.eastmoney.com/EM_UBG_MinuteApi/Js/Get?dtype=all&token=44c9d251add88e27b65ed86506f6e5da&rows=20000&cb=jQuery172002909476607643202_1507706968388&page=1&id='
        url2 = '1&gtvolume=&sort=&_=1507707216623'
        for gupiao_id in url_list:
            url = url1 + str(gupiao_id) + url2
            print('----------------------'+url)
            yield scrapy.Request(url,callback=self.parse_one_data,meta={'gupiao_id':gupiao_id})

    def parse_one_data(self, response):
        print('开始爬取交易明细')
        item = GupiaoOneItem()
        data1 = re.findall(r'data":\["(.*)"\]}',str(response.text))
        data2 = str(data1).replace("['",'')
        data = str(data2).replace("']",'')
        item['one_id'] = response.meta['gupiao_id']
        item['deal_time'] = data
        data_one_list = str(data).split('","')
        for one in data_one_list:
            one_list = one.split(',')
            item['one_id'] = response.meta['gupiao_id']
            item['deal_time'] = one_list[0]
            item['deal_price'] = one_list[1]
            item['deal_num'] = one_list[2]
            item['deal_1'] = one_list[3]
            item['deal_2'] = one_list[4]
            item['deal_3'] = one_list[5]
            item['deal_4'] = one_list[6]
            item['deal_5'] = one_list[7]
            yield item
        print('本次爬取结束')

#
#http://mdfm.eastmoney.com/EM_UBG_MinuteApi/Js/Get?dtype=all&token=44c9d251add88e27b65ed86506f6e5da&rows=20000&cb=jQuery172002909476607643202_1507706968388&page=1&id=6004381&gtvolume=&sort=&_=1507707216623
#
#
#http://mdfm.eastmoney.com/EM_UBG_MinuteApi/Js/Get?dtype=all&token=44c9d251add88e27b65ed86506f6e5da&rows=20000&cb=jQuery172002909476607643202_1507706968388&page=1&id=600438&gtvolume=&sort=&_=1507707216623