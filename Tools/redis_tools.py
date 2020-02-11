# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2018/10/19 10:01

@desc:
http://www.cnblogs.com/melonjiang/p/5342383.html
http://www.cnblogs.com/melonjiang/p/5342505.html
'''

import redis
import config
import json


def keys():
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    result = r.keys()
    if result is None:
        return None
    return result

def get(key):
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    result = r.get(key)
    if result is None:
        return None
    return json.loads(result)

def set(key, val):
    if len(val) == 0:
        return
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    r.set(key, json.dumps(val))


def rm(key):
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    r.delete(key)

# 设置过期时间（秒）
def setex(key, val, time=60):
    if len(val) == 0:
        return
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    r.setex(key, json.dumps(val), time)

# 设置过期时间（毫秒）
def psetex(key, val, time=1000):
    if len(val) == 0:
        return
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    r.psetex(key, time, json.dumps(val))

# 设置新值并返回旧值
def getset(key, val):
    if len(val) == 0:
        return
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    return r.getset(key, json.dumps(val))

# 自增
def incr(key, amount=None):
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    if amount is None:
        return r.incr(key)
    else:
        return r.incr(key, amount=amount)

# 在key对应的list中添加元素，每个新的元素都添加到列表的最左边
def rpush(key, value):
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    r.rpush(key, json.dumps(value))

# 删除列表右侧第一个元素，并返回该值
def lpop(key):
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    return json.loads(r.lpop(key))

def lindex(key, index=0):
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    return json.loads(r.lindex(key, index))

# 返回列表长度
def llen(key):
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    return r.llen(key)

# 分片获取元素
def lrange(key, start, end):
    r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    return r.lrange(key, start, end)




