# -*-coding:utf-8-*-
# odpl行为日志翻译
import ReadConfig
import Log
import time
import ConnectToHtml
import json
# from LogCatch import LogControl
configGet = ReadConfig.ReadConfig()


def isTimeFine(date):
    try:
        if "：" in date or ":" in date:
            return False
        else:
            time.strptime(date, "%Y-%m-%d")
            return True
    except Exception as e:
        print(str(e))
        return False


class getactionlogfromhtml:
    def __init__(self, user_id="", date=""):
        print(user_id, date)
        if user_id == "":
            self.user_id = "34427118"
        else:
            self.user_id = user_id
        if date == "" or not isTimeFine(date):
            self.date = time.strftime("%Y-%m-%d", time.localtime())
        else:
            self.date = date
        self.log = Log.logControl.getLog()
        self.logger = self.log.logger
        headers_list = configGet.getOption("log_headers")
        self.headers = {}
        for i in headers_list:
            self.headers[str(i)] = configGet.get_headers(str(i))
        self.url = "http://p.doras.log.vcinema.cn/realtime/get_terminal_logs.json?user_id=set_id&password=zhuangxulin&date=set_date".replace(
            "set_id", self.user_id).replace("set_date", self.date)
        self.logger.info(self.url)
        self.android_action_keys = json.loads(configGet.GetInfoWhitName("log_keys", "android_action_keys"))
        self.ios_action_keys = json.loads(configGet.GetInfoWhitName("log_keys", "ios_action_keys"))
        self.action_detail_keys = json.loads(configGet.GetInfoWhitName("log_keys", "action_detail_keys"))
        self.ios_Log = json.loads(configGet.GetInfoWhitName("log_keys", "ios_Log"))
        # print(self.action_detail_keys)

    def getlog(self):
        getdata = ConnectToHtml.connecttohtml(url=self.url, headers=self.headers)
        req = getdata.GetHtmlWithOutData()
        return req

    def log_len(self, info):
        try:
            error_keys = []
            info_dic = info.keys()
            iosChannel = ["AppStore", 'TestFlight']
            if info["terminal_info:channel_id"] in iosChannel:
                action_keys = self.ios_action_keys
            else:
                action_keys = self.android_action_keys
            for i in action_keys:
                if i not in info_dic:
                    error_keys.append(i)
            return error_keys
        except Exception as e:
            # print("*" * 1000)
            # print(info)
            # print("*" * 1000)
            # print(str(e))
            self.logger.error(str(e))
            self.logger.error(info)
            return None

    def washLog(self, info):
        try:
            info_list = {}
            info_dic = info.keys()
            if info["action_info:log_type"] == "operate":
                for i in self.ios_Log:
                    if i in info["action_info:action_detail"]:
                        # smqt、ApplicationEnvironment ios端自己维护的日志，不需要我们这边关注
                        info_list["log_record_time"] = (time.strftime("%Y-%m-%d %H:%M:%S",
                                                       time.localtime(int(info["action_info:log_record_time"]) / 1000)))
                        info_list["log_type"] = (info["action_info:log_type"])
                        info_list["action_detail"] = str(info["action_info:action_detail"]) + str("----开发日志无需关注")
                        info_list["channel_id"] = (info["terminal_info:channel_id"])
                        info_list["日志长度"] = (len(info_dic))
                        return info_list
                if "|" in info["action_info:action_detail"]:
                    info_list["log_record_time"] = (time.strftime("%Y-%m-%d %H:%M:%S",
                                                   time.localtime(int(info["action_info:log_record_time"]) / 1000)))
                    info_list["log_type"] = (info["action_info:log_type"])
                    # info_list["action_detail"] = (LogControl.LogControler(info["action_info:action_detail"]))
                    info_list["action_detail"] = (info["action_info:action_detail"])
                    info_list["channel_id"] = (info["terminal_info:channel_id"])
                    info_list["日志长度"] = (len(info_dic))
                    return info_list
                else:
                    info_list["log_record_time"] = (time.strftime("%Y-%m-%d %H:%M:%S",
                                                   time.localtime(int(info["action_info:log_record_time"]) / 1000)))
                    info_list["log_type"] = (info["action_info:log_type"])
                    info_list["action_detail"] = (self.action_detail_keys[info["action_info:action_detail"]])
                    info_list["channel_id"] = (info["terminal_info:channel_id"])
                    info_list["日志长度"] = (len(info_dic))
                    return info_list
            else:
                return None
        except Exception as e:
            # print("*" * 1000)
            # print(info)
            # print("*" * 1000)
            # print(str(e))
            self.logger.error(str(e))
            self.logger.error(info)
            return None

    def getStart(self):
        try:
            return_list = []
            json_data = json.loads(self.getlog().text)
            if json_data["operate_code"] == "200":
                info_list = json_data["operate_result"]["log_list"]
                for i in info_list:
                    info = self.washLog(i)
                    if info is None:
                        continue
                    else:
                        return_list.append(info)
                        text = self.log_len(i)
                        if len(text) != 0:
                            return_list.append(i)
                            return_list.append(text)
            else:
                return_list.append("数据返回结果异常！错误码：" + str(json_data["operate_code"]))
                self.logger.error("数据返回结果异常！错误码：" + str(json_data["operate_code"]))
            print(return_list)
            return {"data": return_list}
        except Exception as e:
            self.logger.error(str(e))
            return str(e)


if __name__ == '__main__':
    a = getactionlogfromhtml(user_id="48667240", date="2021-11-08")
    info_list = a.getStart()
    for i in info_list['data']:
        print(i)
