# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/12/3 17:27

@desc:

'''

from Tools import public_tools
import logging
from roborts.brush_flow_robot_exapi import BrushFlowRobot

if __name__ == '__main__':
    exapi = public_tools.get_exapi("bitmex", {
        'enableRateLimit': False,
        'timeout': 20000,
        'proxies': {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}
    })
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    robot = BrushFlowRobot(exapi, None, {
        'symbol': 'BTC/USD',
        'logger': logger,
        'module': "1"
    })
    robot.start()