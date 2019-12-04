# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/12/3 17:22

@desc: 刷量机器人

'''


class BrushFlowRobot(object):
    exapi = None
    exws = None
    module = None
    start_time = None
    end_time = None


    def __init__(self, exapi, module, exws=None, params={}):
        self.exapi = exapi
        self.exws = exws
        self.module = module
        for key in params:
            if hasattr(self, key) and isinstance(getattr(self, key), dict):
                setattr(self, key, self.deep_extend(getattr(self, key), params[key]))
            else:
                setattr(self, key, params[key])

    def start(self):
        pass

    def exit(self):
        pass

    @staticmethod
    def deep_extend(*args):
        result = None
        for arg in args:
            if isinstance(arg, dict):
                if not isinstance(result, dict):
                    result = {}
                for key in arg:
                    result[key] = BrushFlowRobot.deep_extend(result[key] if key in result else None, arg[key])
            else:
                result = arg
