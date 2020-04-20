# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/12/11 10:18

@desc:

'''

import logging
import asyncio
import traceback

class ExApiRobot(object):

    def __init__(self, exapi, module, params={}):
        self.exapi = exapi
        self.module = module
        self.logger = logging.getLogger('root')
        self.is_ready = False
        for key in params:
            if hasattr(self, key) and isinstance(getattr(self, key), dict):
                setattr(self, key, self.deep_extend(getattr(self, key), params[key]))
            else:
                setattr(self, key, params[key])

    async def schedule_job(self, func, schedule_time):
        fail_times = 0
        while self.is_ready:
            try:
                await func
                fail_times = 0
            except:
                self.logger.error("schedule job run error:%s" % str(traceback.format_exc()))
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                await asyncio.sleep(schedule_time)

    def async_task(self, task=[]):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.gather(*task))
        except:
            self.logger.error("async task run error:%s" % str(traceback.format_exc()))
        finally:
            loop.close()

    @staticmethod
    def deep_extend(*args):
        result = None
        for arg in args:
            if isinstance(arg, dict):
                if not isinstance(result, dict):
                    result = {}
                for key in arg:
                    result[key] = ExApiRobot.deep_extend(result[key] if key in result else None, arg[key])
            else:
                result = arg
