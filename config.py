# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2018/9/17 20:27

@desc: config

'''

# 数据库
DB_USER = 'root'
DB_PASSWORD = ''
DB_HOST = '127.0.0.0'
DB_PORT = 3306
DB_NAME = 'test'
DATABASE_URI = 'mysql+pymysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + str(
    DB_PORT) + '/' + DB_NAME + '?charset=utf8&autocommit=true'

# Redis
REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_PASSWORD = ''

# MongoDB
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
