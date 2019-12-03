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
from Tools import PublicTools


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
            print('\n', PublicTools.getTime(), "mongo连接成功")
        except BaseException as e:
            print('\n', PublicTools.getTime(), 'mongo连接失败：', e.args[0], e.args[1])

    def close(self):
        self.client.close()

    def insertOne(self, obj):
        result = self.collection.insert_one(obj)
        return result

    def insertMany(self, lists):
        results = self.collection.insert_many(lists)
        return results

    def findOne(self, condition, id=None):
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
