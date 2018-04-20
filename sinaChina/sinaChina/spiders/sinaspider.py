# -*- coding: utf-8 -*-
import scrapy
from sinaChina.items import SinachinaItem
import requests
from lxml import etree
import copy


class SinaspiderSpider(scrapy.Spider):
    name = 'sinaspider2.0'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    # 获取三级页链接
    def parse(self, response):
        parenturls = response.xpath("//div[@class='clearfix']")
        # 遍历大类
        item = SinachinaItem()
        for parenturl in parenturls[:2]:

            if len(parenturl.xpath("./h3/a/text()")) != 0:
                level1 = parenturl.xpath("./h3/a/text()").extract()[0]
            else:
                if len(parenturl.xpath("./h3/span/text()")) != 0:
                    level1 = parenturl.xpath("./h3/span/text()").extract()[0]
                else:
                    level1 = parenturl.xpath("./h3/text()").extract()[0]
            # 一级目录名称
            print(level1)

            # 遍历二级目录
            lines = parenturl.xpath("./ul/li")
            for line in lines[:5]:
                level2 = line.xpath('./a/text()').extract()[0]
                print("----", level2)

                try:
                    response = requests.get(line.xpath('./a/@href').extract()[0])
                    html = etree.HTML(response.content.decode('utf-8', 'ignore'))
                    # 遍历三级目录
                    datas = html.xpath("//div[@class=\"second-nav\"]/div/div//a")

                    for data in datas:
                        level3 = data.xpath("./text()")[0]
                        print('--------', level3)
                        item['level1'] = level1
                        item['level2'] = level2
                        item['level3'] = level3
                        item['url'] = data.xpath("./@href")[0]
                        yield scrapy.Request(item['url'], meta={"meta": copy.deepcopy(item)},
                                             callback=self.parse_level3,
                                             dont_filter=True)
                except Exception:
                    pass

    def parse_level3(self, response):
        item = response.meta['meta']
        datas = response.xpath("//ul[@class='list_009']/li")
        for data in datas:
            url = data.xpath("./a/@href").extract()[0]
            yield scrapy.Request(url, meta={"meta2": item}, callback=self.parse_content, dont_filter=True)

            # # 获取下一页
            # url = response.url
            # next_page = response.xpath("//span[@class='pagebox_next'][1]/a/@href").extract()[0]
            # next_page = next_page[2:]
            # url_list = url.split('/')
            # newurl = ''
            # for i in range(len(url_list) - 1):
            #     newurl += url_list[i]
            #     newurl += "/"
            # newurl += next_page
            # # 自动翻页
            # if len(response.xpath("//ul[@class='list_009']//li")) != 0:
            #     yield scrapy.Request(newurl, meta={'meta': item}, callback=self.parse)

    def parse_content(self, response):
        item = response.meta['meta2']
        try:
            item['title'] = \
                response.xpath("//div[@class='main-content w1240']/h1[@class='main-title']/text()").extract()[0]
            lines = response.xpath("//div[@class='article']/p/text()").extract()
            content = ''
            for line in lines:
                content += line + '\n'
                item['content'] = content
        except Exception:
            item['title'] = ''
            item['content'] = ''
        yield item
