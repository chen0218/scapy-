# -*- coding: utf-8 -*-
import scrapy
from gupiao.items import GupiaoItem
from gupiao.items import GupiaoAllItem
from bs4 import BeautifulSoup
import re
import random

class AllGupiaoSpider(scrapy.Spider):
    name = "all_gupiao"
#    allowed_domains = [""]
    start_urls = ['http://quote.eastmoney.com/stocklist.html']

    user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

    def parse(self, response):
        item = GupiaoItem()
        #设置表头
        item1 = GupiaoAllItem()
        item1['gp_name'] = '股票名和编码'
        item1['gp_start_price'] = '开盘价'
        item1['gp_cjl'] = '成交量'
        item1['gp_cje'] = '成交额'
        item1['gp_max'] = '最高'
        item1['gp_min'] = '最低'
        item1['gp_yesterday_price'] = '昨收'
        item1['gp_zf'] = '振幅'
        item1['gp_np'] = '内盘'
        item1['gp_wp'] = '外盘'
        item1['gp_wb'] = '委比'
        item1['gp_lb'] = '量比'
        item1['gp_hsl'] = '换手率'
        item1['gp_zsz'] = '总市值'
        item1['gp_ltsz'] = '流通市值'
        item1['gp_sjl'] = '市净率'
        item1['gp_ltgb'] = '流通股本'
        item1['gp_syl'] = '市盈率'
        item1['gp_zgb'] = '总股本'
        item1['gp_mgjzc'] = '每股净资产'
        yield item1
        soup = BeautifulSoup(response.text, 'html.parser')
        a = soup.find_all('a')
        ua = random.choice(self.user_agent_list)#随机抽取User-Agent
        headers = {
          'Accept-Encoding':'gzip, deflate, sdch, br',
          'Accept-Language':'zh-CN,zh;q=0.8',
          'Connection':'keep-alive',
          'Referer':'https://gupiao.baidu.com/',
          'User-Agent':ua
          }#构造请求头
#                循环获取每个股票的代号并组成url
        for i in a:
            try:
                href = i.attrs['href']
                gpid = re.findall(r"[s][hz][06]\d{5}", href)[0]
                item['gp_name_and_id']= i.string
                url = 'https://gupiao.baidu.com/stock/' + str(gpid) +".html"
                yield scrapy.Request(url,callback=self.parse_all_gupiao,headers=headers,meta={'name':i.string,'url':url})
                yield item
            except:
                continue


    def parse_all_gupiao(self,response):
        item = GupiaoAllItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        stockInfo = soup.find('div',attrs={'class':'stock-bets'})
        valueList = stockInfo.find_all('dd')
        item['gp_name'] = response.meta['name']
        item['gp_start_price'] = valueList[0].text
        item['gp_cjl'] = valueList[1].text
        item['gp_cje'] = valueList[5].text
        item['gp_max'] = valueList[2].text
        item['gp_min'] = valueList[13].text
        item['gp_yesterday_price'] = valueList[11].text
        item['gp_zf'] = valueList[16].text
        item['gp_np'] = valueList[4].text
        item['gp_wp'] = valueList[15].text
        item['gp_wb'] = valueList[6].text
        item['gp_lb'] = valueList[17].text
        item['gp_hsl'] = valueList[12].text
        item['gp_zsz'] = valueList[18].text
        item['gp_ltsz'] = valueList[7].text
        item['gp_sjl'] = valueList[19].text
        item['gp_ltgb'] = valueList[21].text
        item['gp_syl'] = valueList[8].text
        item['gp_zgb'] = valueList[10].text
        item['gp_mgjzc'] = valueList[20].text
        yield item


