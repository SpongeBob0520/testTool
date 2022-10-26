# -*-coding:utf-8-*-
# 日志类，看看就行，别动
import logging
import threading
import ReadConfig
import os
from datetime import datetime


class Log:
    def __init__(self):
        global logPath, configGet, fileRealPath
        fileRealPath = ReadConfig.fileRealPath
        logPath = os.path.join(fileRealPath, 'LogFiles')
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        logPath = os.path.join(logPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        self.logger = logging.getLogger()  # 初始化logger对象
        self.logger.setLevel(logging.INFO)  # 设置日志等级为info等级，就是不管是啥都给你记录
        handler = logging.FileHandler(os.path.join(logPath, "output.log"), mode='a', encoding='utf-8')  # 设置日志文件保存地址
        # print(os.path.join(logPath, "output.log"))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # 设置日志格式
        handler.setFormatter(formatter)
        PrintToStream = logging.StreamHandler()
        PrintToStream.setLevel(logging.INFO)
        self.logger.addHandler(PrintToStream)
        # 日志输出到控制台展示，info等级
        self.logger.addHandler(handler)


class logControl:
    log = None
    LogLock = threading.Lock()
    def __init__(self):
        pass
    @staticmethod
    def getLog():
        if logControl.log is None:
            logControl.LogLock.acquire()
            logControl.log = Log()
            logControl.LogLock.release()
        return logControl.log

# git remote add origin https://github.com/SpongeBob0520/Test.git
# git push -u origin master
