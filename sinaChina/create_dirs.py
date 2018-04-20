import os
import requests
from lxml import etree

url = "http://news.sina.com.cn/guide/"
basedir = os.path.join(os.getcwd(), 'data')

response = requests.get(url)
html = etree.HTML(response.content.decode('utf-8'))

parenturls = html.xpath("//div[@class='clearfix']")
# 遍历大类
# 一级目录
for parenturl in parenturls:
    if len(parenturl.xpath("./h3/a/text()")) != 0:
        print(parenturl.xpath("./h3/a/text()"))
        level1_path = basedir + '\\' + parenturl.xpath("./h3/a/text()")[0]
    else:
        if len(parenturl.xpath("./h3/span/text()")) != 0:
            print(parenturl.xpath("./h3/span/text()"))
            level1_path = basedir + '\\' + parenturl.xpath("./h3/span/text()")[0]
        else:
            print(parenturl.xpath("./h3/text()"))
            level1_path = basedir + '\\' + parenturl.xpath("./h3/text()")[0]
    os.mkdir(level1_path)

    # 遍历小类
    # 二级目录
    lines = parenturl.xpath("./ul/li")
    for line in lines:
        print("----", line.xpath('./a/text()'))
        level2_path = level1_path + '\\' + line.xpath('./a/text()')[0]
        os.mkdir(level2_path)
        # 三级目录
        try:
            response = requests.get(line.xpath('./a/@href')[0])
            html = etree.HTML(response.content.decode('utf-8', 'ignore'))
            # 三级类
            # 三级目录
            datas = html.xpath("//div[@class='wrap clearfix']/div[@class='links']/a")
            for data in datas:
                print('--------', data.xpath("./text()"))
                level3_path = level2_path + '\\' + data.xpath("./text()")[0]
                os.mkdir(level3_path)
        except Exception:
            pass
    print('')
