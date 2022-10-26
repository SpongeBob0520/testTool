# -*-coding:utf-8-*-
# 网络连接请求类，基础类
import requests
import ReadConfig
import Log

configGet = ReadConfig.ReadConfig()


class connecttohtml:
    def __init__(self, url="", headers="", data=""):
        if url == "":
            self.url = "http://www.baidu.com"
        else:
            self.url = url
        if headers == "":
            self.headers = {"content-type": "application/json"}
        else:
            self.headers = headers
        if data == "":
            self.data = {"page": "0"}
        else:
            self.data = data
        self.log = Log.logControl.getLog()
        self.logger = self.log.logger
        

    def GetHtmlWithOutData(self):
        try:
            # print("GetHtmlWithOutData")
            req = requests.get(url=self.url, headers=self.headers, timeout=60)
            self.logger.info(self.url)
            self.logger.info(req.status_code)
            return req
        except Exception as e:
            self.logger.error("#"*100)
            self.logger.error(self.url)
            self.logger.error(self.headers)
            self.logger.error(str(e))
            self.logger.error("#" * 100)
            return False

    def GetHtmlWithData(self):
        # print("GetHtmlWithData")
        try:
            req = requests.get(url=self.url, headers=self.headers, data=self.data, timeout=60)
            self.logger.info(self.url)
            self.logger.info(req.status_code)
            return req
        except Exception as e:
            self.logger.error("#" * 100)
            self.logger.error(self.url)
            self.logger.error(self.headers)
            self.logger.error(self.data)
            self.logger.error(req.status_code)
            self.logger.error(str(e))
            self.logger.error("#" * 100)
            return False

    def PostHtml(self):
        try:
            req = requests.post(url=self.url, headers=self.headers, data=self.data, timeout=60)
            self.logger.info(self.url)
            self.logger.info(req.status_code)
            return req
        except Exception as e:
            self.logger.error("#"*100)
            self.logger.error(self.url)
            self.logger.error(self.headers)
            self.logger.error(self.data)
            self.logger.error(str(e))
            self.logger.error("#" * 100)
            return False



