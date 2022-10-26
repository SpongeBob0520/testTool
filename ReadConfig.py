# -*-coding:utf-8-*-
# 读配置文件的底层类，别动
import configparser
import os
from datetime import datetime

fileRealPath = os.path.split(os.path.realpath(__file__))[0]
configFilePath = os.path.join(fileRealPath, "config.ini")


class ReadConfig:
    def __init__(self):
        self.Time_now = datetime.now()
        self.fileOpen = configparser.RawConfigParser()
        self.fileOpen.read(configFilePath, encoding='utf-8')

    # 根据sectionName获取改sectionName下所有的子项名字，做列表返回
    def getOption(self, sectionName):
        try:
            return self.fileOpen.options(sectionName)
        except Exception as e:
            print("Error !", str(e))
            return self.fileOpen.options("error")

    def get_db(self, name):
        values = self.fileOpen.get("Mysql", name)
        return values

    def get_headers(self, name):
        values = self.fileOpen.get("log_headers", name)
        return values

    def get_data(self, name):
        values = self.fileOpen.get("Aliyun_data", name)
        return values

    def GetInfoWhitName(self, sectionName, name):
        values = self.fileOpen.get(sectionName, name)
        return values

    def GetTestMongoDB(self):
        databaseconnect = {}
        databaseconnect['host'] = self.fileOpen.get('Test_MongoDB', 'host')
        databaseconnect['database'] = self.fileOpen.get('Test_MongoDB', 'database')
        databaseconnect['port'] = self.fileOpen.get('Test_MongoDB', 'port')
        databaseconnect['username'] = self.fileOpen.get('Test_MongoDB', 'username')
        databaseconnect['passwrod'] = self.fileOpen.get('Test_MongoDB', 'passwrod')
        return databaseconnect

    def GetOnlineMongoDB(self):
        databaseconnect = {}
        databaseconnect['host'] = self.fileOpen.get('online_MongoDB', 'host')
        databaseconnect['database'] = self.fileOpen.get('online_MongoDB', 'database')
        databaseconnect['port'] = self.fileOpen.get('online_MongoDB', 'port')
        databaseconnect['username'] = self.fileOpen.get('online_MongoDB', 'username')
        databaseconnect['passwrod'] = self.fileOpen.get('online_MongoDB', 'passwrod')
        return databaseconnect

    def GetTestMySql(self):
        databaseconnect = {}
        databaseconnect['host'] = self.fileOpen.get('Test_MySql', 'host')
        databaseconnect['database'] = self.fileOpen.get('Test_MySql', 'database')
        databaseconnect['username'] = self.fileOpen.get('Test_MySql', 'username')
        databaseconnect['passwrod'] = self.fileOpen.get('Test_MySql', 'passwrod')
        return databaseconnect

    def GetOnlineMySql(self):
        databaseconnect = {}
        databaseconnect['host'] = self.fileOpen.get('online_MySql', 'host')
        databaseconnect['database'] = self.fileOpen.get('online_MySql', 'database')
        databaseconnect['username'] = self.fileOpen.get('online_MySql', 'username')
        databaseconnect['passwrod'] = self.fileOpen.get('online_MySql', 'passwrod')
        return databaseconnect

    # def get_login(self):
    #     data = {'user': '', 'pwd': '', 'captcha': ''}
    #     for i in data.keys():
    #         data[i] = self.fileOpen.get("login", str(i))
    #     url = self.fileOpen.get("login", 'url')
    #     return data, url

    # def CookiesWrite(self, cookies):
    #     self.fileOpen.set("web-headers", "cookie", str(cookies))
    #     self.fileOpen.write(open(configFilePath, 'r+', encoding='utf-8'))
    #     return True
    #     写入到配置文件





