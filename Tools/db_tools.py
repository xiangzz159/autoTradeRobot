# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/5/10 21:18

@desc: https://cloud.tencent.com/developer/article/1151814

'''

import pymongo
from bson.objectid import ObjectId
from Tools import public_tools
import redis
import json
import pymysql


class MongoClient(object):
    def __init__(self, host, port, db, collection):
        self.host = host
        self.port = port
        self.db = db
        self.collection = collection

    def conn(self):
        try:
            self.client = pymongo.MongoClient(host=self.host, port=self.port)
            self.db = self.client[self.db]
            self.collection = self.db[self.collection]
            print('\n', public_tools.get_time(), "mongo连接成功")
        except BaseException as e:
            print('\n', public_tools.get_time(), 'mongo连接失败：', e.args[0], e.args[1])

    def close(self):
        self.client.close()

    def insert_one(self, obj):
        result = self.collection.insert_one(obj)
        return result

    def insert_many(self, lists):
        results = self.collection.insert_many(lists)
        return results

    def find_one(self, condition, id=None):
        result = self.collection.find_one({'_id': ObjectId(id)}) if id else self.collection.find_one(condition)
        return result

    def find(self, conditions):
        results = self.collection.find(conditions)
        return results

    def update(self, condition, new_obj):
        result = self.collection.update(condition, new_obj)
        return result

    def remove(self, condition):
        result = self.collection.remove(condition)
        return result


class RedisClient(object):
    def __init__(self, host, port, password=None):
        self.host = host
        self.port = port
        self.password = password

    def conn(self):
        try:
            self.client = redis.Redis(host=self.host, port=self.port, password=self.password, decode_responses=True)
            print('\n', public_tools.get_time(), "redis连接成功")
        except BaseException as e:
            print('\n', public_tools.get_time(), 'redis连接失败：', e.args[0], e.args[1])

    def close(self):
        self.client.connection_pool.disconnect()

    def keys(self):
        result = self.client.keys()
        if result is None:
            return None
        return result

    def get(self, key):
        result = self.client.get(key)
        if result is None:
            return None
        return json.loads(result)

    def set(self, key, val):
        if len(val) == 0:
            return
        self.client.set(key, json.dumps(val))

    def rm(self, key):
        self.client.delete(key)

    # 设置过期时间（秒）
    def setex(self, key, val, time=60):
        if len(val) == 0:
            return
        self.client.setex(key, json.dumps(val), time)

    # 设置过期时间（毫秒）
    def psetex(self, key, val, time=1000):
        if len(val) == 0:
            return
        self.client.psetex(key, time, json.dumps(val))

    # 设置新值并返回旧值
    def getset(self, key, val):
        if len(val) == 0:
            return
        return self.client.getset(key, json.dumps(val))

    # 自增
    def incr(self, key, amount=None):
        if amount is None:
            return self.client.incr(key)
        else:
            return self.client.incr(key, amount=amount)

    # 在key对应的list中添加元素，每个新的元素都添加到列表的最左边
    def rpush(self, key, value):
        self.client.rpush(key, json.dumps(value))

    # 删除列表右侧第一个元素，并返回该值
    def lpop(self, key):
        return json.loads(self.client.lpop(key))

    def lindex(self, key, index=0):
        return json.loads(self.client.lindex(key, index))

    # 返回列表长度
    def llen(self, key):
        return self.client.llen(key)

    # 分片获取元素
    def lrange(self, key, start, end):
        return self.client.lrange(key, start, end)


class MysqlClient(object):
    # 初始化方法
    def __init__(self, host, port, user, password, db, charsets='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charsets = charsets

    # 链接数据库
    def conn(self):
        try:
            self.db = pymysql.Connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                charset=self.charsets
            )
            self.cursor = self.db.cursor()
            print('\n', public_tools.get_time(), 'mysql连接成功')
        except BaseException as e:
            print('\n', public_tools.get_time(), 'mysql连接失败：', e.args[0], e.args[1])

    # 关闭连接
    def close(self):
        self.cursor.close()
        self.db.close()

    # 查询单行记录
    def get_one(self, sql):
        res = None
        try:
            self.conn()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
        except BaseException as e:
            print('\n', public_tools.get_time(), '查询失败, error:', e.args[0], e.args[1])
        return res

    # 查询列表数据
    def get_all(self, sql):
        res = None
        try:
            self.conn()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except BaseException as e:
            print('\n', public_tools.get_time(), '查询失败, error:', e.args[0], e.args[1])
        return res

    def __execute(self, sql):
        count = 0
        try:
            self.conn()
            count = self.cursor.execute(sql)
            self.db.commit()
            self.close()
        except BaseException as e:
            print('\n', public_tools.get_time(), '操作失败, error:', e.args[0], e.args[1])
            self.db.rollback()
        return count

    # 插入数据
    def insert(self, sql):
        return self.__execute(sql)

    # 修改数据
    def edit(self, sql):
        return self.__execute(sql)

    # 删除数据
    def delete(self, sql):
        return self.__execute(sql)

    # 更新数据
    def update(self, sql):
        return self.__execute(sql)
