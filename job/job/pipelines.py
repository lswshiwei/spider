# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql,pymongo


class JobPipeline(object):
    def process_item(self, item, spider):
        print(__file__, item)
        return item


class Job_Mongodb_Pipeline(object):
    # 连接数据库
    def __init__(self):
        self.client = pymongo.MongoClient(host='47.104.128.150', port=27017)
        self.db = self.client['jobssss']
        self.collection = self.db['jobs']

    # 插入数据到数据库
    def process_item(self, item, spider):
        dict_item = dict(item)
        self.collection.insert(dict_item)
        return item
    # 关闭数据库连接
    def close_spider(self, spider):
        self.client.close()



class Job_Mysql_Pipeline(object):
    # 连接数据库
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user = 'root',
            password = '0321',
            db = 'jobs',
            charset = 'utf8')
        self.curor = self.conn.cursor()
    # 插入数据到数据库
    def process_item(self, item, spider):
        sql = 'insert into job(`name`, company,money,address) VALUES (%s,%s,%s,%s )'
        self.curor.execute(sql,(item['name'], item['company'],item['money'], item['address']))
        self.conn.commit()
        print(__file__, item)
        return item
    # 关闭数据库连接
    def close_spider(self,spider):
        self.curor.close()
        self.conn.close()