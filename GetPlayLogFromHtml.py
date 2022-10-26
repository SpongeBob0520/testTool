# -*-coding:utf-8-*-
# odps 播放日志翻译

import ReadConfig
import Log
import time
import ConnectToHtml
import json

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


class getplaylogfromhtml:
    def __init__(self, user_id="", date=""):
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
        self.play_keys = json.loads(configGet.GetInfoWhitName("log_keys", "play_keys"))
        self.operate_type_dic = json.loads(configGet.GetInfoWhitName("log_keys", "operate_type_dic"))
        self.view_source_dic = json.loads(configGet.GetInfoWhitName("log_keys", "view_source_dic"))
        self.play_type = json.loads(configGet.GetInfoWhitName("log_keys", "play_type"))

    def getlog(self):
        getdata = ConnectToHtml.connecttohtml(url=self.url, headers=self.headers)
        req = getdata.GetHtmlWithOutData()
        return req

    def log_len(self, info):
        try:
            error_keys = []
            info_dic = info.keys()
            for i in self.play_keys:
                if i not in info_dic:
                    error_keys.append(i)
            return error_keys
        except Exception as e:
            # print("*" * 100)
            # print(info)
            # print("*" * 100)
            # print(str(e))
            self.logger.error(str(e))
            self.logger.error(info)
            return None

    def washLog(self, info):
        try:
            info_list = {}
            broadcast = ["play", "mini_play", "mini_live_broadcast", "live_broadcast", "play_trailer"]
            info_dic = info.keys()
            if info["action_info:log_type"] in broadcast:
                info_list["log_record_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(info["action_info:log_record_time"]) / 1000))
                if "127.0.0.1" in info['action_info:movie_url']:
                    info_list["movie_url"] = '播放地址异常---' + str(info['action_info:movie_url'])
                else:
                    info_list["movie_url"] = '播放地址正常---' + str(info['action_info:movie_url'])
                info_list["p2p_status"] = info["action_info:p2p_status"]
                info_list["movie_id"] = info["action_info:movie_id"]
                info_list["log_type"] = self.play_type[info["action_info:log_type"]]
                info_list["operate_type"] = self.operate_type_dic[info["action_info:operate_type"]]
                info_list["play_total_time"] = info["action_info:play_total_time"]
                if info["action_info:view_source"] in self.view_source_dic.keys():
                    info_list["view_source"] = self.view_source_dic[info["action_info:view_source"]]
                else:
                    info_list["view_source"] = (info["action_info:view_source"])
                info_list["channel_id"] = (info["terminal_info:channel_id"])
                info_list["日志长度"] = (len(info_dic))
                return info_list
            else:
                return None
        except Exception as e:
            # print("*" * 100)
            # print(info)
            # print("*" * 100)
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
            return {"data": return_list}
        except Exception as e:
            self.logger.error(str(e))
            return {"error": str(e)}


if __name__ == '__main__':
    a = getplaylogfromhtml(user_id="48667240", date="2021-11-08")
    info_list = a.getStart()['data']
    for i in info_list:
        print(i)
    # a = '2021-10-27 19:12:32:849'
    # b = datetime.strptime(a, "%Y-%m-%d %H:%M:%S:%f")
    # print(int(time.mktime(b.timetuple()) * 1000.0 + b.microsecond / 1000.0))