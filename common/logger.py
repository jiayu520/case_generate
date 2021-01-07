import logging
import os
import time

import colorlog

cur_path = os.path.dirname(os.path.realpath(__file__)) #存放日志路径
log_path = os.path.join(os.path.dirname(cur_path),'logs')
if not os.path.exists(log_path):
    os.mkdir(log_path) #如果不存在这个文件夹，自动创建
logName = os.path.join(log_path,'%s.log' % time.strptime('%Y-%m-%s')) #文件的命名

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}

class Log:
    def __init__(self,logName=logName):
        self.logName = logName
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = colorlog.