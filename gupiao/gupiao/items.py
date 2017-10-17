# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GupiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    gp_name_and_id = scrapy.Field()   #股票编号和名称

class GupiaoAllItem(scrapy.Item):
    gp_name = scrapy.Field()    #当前股票名称
    gp_start_price = scrapy.Field() #今天开盘价
    gp_cjl = scrapy.Field() #成交量
    gp_cje  = scrapy.Field()    #成交额
    gp_max  = scrapy.Field()    #最高
    gp_min  = scrapy.Field()    #最低
    gp_yesterday_price = scrapy.Field()   #昨天收盘价
    gp_zf  = scrapy.Field()   #振幅
    gp_np  = scrapy.Field()    #内盘
    gp_wp = scrapy.Field()    #外盘
    gp_wb  = scrapy.Field()    #委比
    gp_lb  = scrapy.Field()   #量比
    gp_hsl  = scrapy.Field()   #换手率
    gp_zsz  = scrapy.Field()   #总市值
    gp_ltsz  = scrapy.Field()   #流通市值
    gp_sjl  = scrapy.Field()   #市净率
    gp_ltgb  = scrapy.Field()   #流通股本
    gp_syl  = scrapy.Field()   #市盈率
    gp_zgb  = scrapy.Field()   #总股本
    gp_mgjzc  = scrapy.Field()   #每股净资产


class GupiaoOneItem(scrapy.Item):
    one_id = scrapy.Field()
    deal_time = scrapy.Field()   #交易时间
    deal_price = scrapy.Field()    #交易价格
    deal_num = scrapy.Field()     #交易数量
    deal_1 = scrapy.Field()
    deal_2 = scrapy.Field()
    deal_3 = scrapy.Field()
    deal_4 = scrapy.Field()
    deal_5 = scrapy.Field()