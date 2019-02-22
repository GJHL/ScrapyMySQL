# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi


# 同步更新操作
# class LvyouPipeline(object):
#     def __init__(self):
#         # connection database
#         self.connect = pymysql.connect(host='MYSQL_HOST', user='MYSQL_USER', passwd='MYSQL_PASSWORD', db='MYSQL_DBNAME')  # 后面三个依次是数据库连接名、数据库密码、数据库名称
#         # get cursor
#         self.cursor = self.connect.cursor()
#         print("连接数据库成功")
#
#     def process_item(self, item, spider):
#         # sql语句
#         insert_sql = """
#         insert into lvyou(name1, address, grade, score, price) VALUES (%s,%s,%s,%s,%s)
#         """
#         # 执行插入数据到数据库操作
#         self.cursor.execute(insert_sql, (item['Name'], item['Address'], item['Grade'], item['Score'],
#                                          item['Price']))
#         # 提交，不进行提交无法保存到数据库
#         self.connect.commit()
#
#     def close_spider(self, spider):
#         # 关闭游标和连接
#         self.cursor.close()
#         self.connect.close()


# 异步更新操作
class LvyouPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )

        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        """
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常

    def do_insert(self, cursor, item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        insert_sql = """
        insert into lvyou(name1, address, grade, score, price) VALUES (%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item['Name'], item['Address'], item['Grade'], item['Score'],
                                                  item['Price']))

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print(failure)
