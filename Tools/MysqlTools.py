# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/12/3 23:17

@desc:

'''

import pymysql
from Tools import PublicTools


class MysqlClient():
    # 初始化方法
    def __init__(self, host, port, user, passwd, dbName, charsets='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbName = dbName
        self.charsets = charsets

    # 链接数据库
    def conn(self):
        try:
            self.db = pymysql.Connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.passwd,
                db=self.dbName,
                charset=self.charsets
            )
            self.cursor = self.db.cursor()
            print('\n', PublicTools.getTime(), 'mysql连接成功')
        except BaseException as e:
            print('\n', PublicTools.getTime(), 'mysql连接失败：', e.args[0], e.args[1])

    # 关闭连接
    def close(self):
        self.cursor.close()
        self.db.close()

    # 查询单行记录
    def getOne(self, sql):
        res = None
        try:
            self.getCon()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
        except BaseException as e:
            print('\n', PublicTools.getTime(), '查询失败, error:', e.args[0], e.args[1])
        return res

    # 查询列表数据
    def getAll(self, sql):
        res = None
        try:
            self.getCon()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except BaseException as e:
            print('\n', PublicTools.getTime(), '查询失败, error:', e.args[0], e.args[1])
        return res

    # 插入数据
    def __insert(self, sql):
        count = 0
        try:
            self.getCon()
            count = self.cursor.execute(sql)
            self.db.commit()
            self.close()
        except BaseException as e:
            print('\n', PublicTools.getTime(), '操作失败, error:', e.args[0], e.args[1])
            self.db.rollback()
        return count

    # 修改数据
    def __edit(self, sql):
        return self.__insert(sql)

    # 删除数据
    def __delete(self, sql):
        return self.__insert(sql)

    # 更新数据
    def __update(self, sql):
        return self.__insert(sql)
