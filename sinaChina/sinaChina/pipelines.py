# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

Base_dir = os.path.join(os.path.dirname(os.getcwd()), 'data')


class SinachinaPipeline(object):
    def process_item(self, item, spider):
        filedirPath = Base_dir + '\\'
        filedirPath += item['level1']

        if item['level2'] != '':
            filedirPath += '\\'
            filedirPath += item['level2']

            if item['level3'] != '' and item['title'] != '':
                filedirPath += '\\'
                filedirPath += item['level3']

                filename = filedirPath + '\\' + item['title'] + '.txt'
                with open(filename, 'wb') as f:
                    f.write(item['content'].encode('utf-8'))
                return item
