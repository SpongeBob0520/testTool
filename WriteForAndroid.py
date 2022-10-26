# 验证线上打包情况并发送到钉钉，别动他
import requests
import json
import hashlib
import base64
import time
import hmac
import urllib
# import sys


class writeForMeiQi:
    def __init__(self, bbh, build_code):
        self.bbh = str(bbh)
        self.build_code = str(build_code)
        self.url = 'https://update.app.vcinema.cn/PumpkinFilm-aph-bbh-build-build_code-release-sign.apk'
        self.url = self.url.replace("bbh", self.bbh)
        self.url = self.url.replace("build_code", self.build_code)
        path = self.url.replace("https://update.app.vcinema.cn", '')
        self.headers = {
            "authority": "update.app.vcinema.cn",
            "method": "GET",
            "path": path,
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "cookie": "phone=13732491375; userName=jiangnanqiang",
            "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }
        self.getHtml()

    def signGet(self):
        token = "1bfa1db83ae8f228b1ad48c80263b26e020277735fed798938f60d847dfba990"
        timestamp = str(round(time.time() * 1000))
        secret = 'SECfdf195a9b733bad5401aef756f1aed48c04c1a822a7b4bf7ff0d9dd3c619cc96'# 这里填写机器人给你的那个签名
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        url = "https://oapi.dingtalk.com/robot/send?access_token=" + str(token) + "&timestamp=" + str(timestamp) + "&sign=" + str(sign)
        return url

    def sendActionCard(self, data_dic):
        headers = {"content-type": "application/json"}
        btns = []
        for info in data_dic.keys():
            # https://update.app.vcinema.cn/PumpkinFilm-aph100-5.7.0-build-2446-beta-sign.apk
            # https://update.app.vcinema.cn/PumpkinFilm-aph100-5.7.0-build-2446-beta.apk
            title_sign = info + "-" + self.bbh + "-" + self.build_code + "-sign-" + str(data_dic[info]['WithSign'])
            title = info + "-" + self.bbh + "-" + self.build_code + "-" + str(data_dic[info]['WithOutSign'])
            apkWithSign_Url = data_dic[info]['WithSign_url']
            apkWithOutSign_url = data_dic[info]['WithOutSign_url']
            info_dict_sign = {"title": title_sign, "actionURL": apkWithSign_Url}
            info_dict = {"title": title, "actionURL": apkWithOutSign_url}
            btns.append(info_dict_sign)
            btns.append(info_dict)
        data = {
            "msgtype": "actionCard",
            "actionCard":
                {
                    "title": "线上android打包情况",
                    "text": "读万卷书，行万里路",
                    "hideAvatar": "0",
                    "btnOrientation": "0",
                    "btns": '',
                }
        }
        for i in range(0, len(btns) // 10):
            url = self.signGet()
            if i == len(btns) // 10 + 1:
                time.sleep(0.1)
                info_list = btns[i * 10: -1]
            else:
                time.sleep(0.1)
                info_list = btns[(i * 10): (i * 10) + 10]
            data['actionCard']["btns"] = info_list
            # print(data)
            String_textMsg = json.dumps(data)
            # print(String_textMsg)
            res = requests.post(url=url, headers=headers, data=String_textMsg)
            print(res.text)

    def getHtml(self):
        data = {}
        headers_sign = self.headers
        aph_list = ["0", "1", "3", "4", "7", "9", "10", "12", "13", "14", "32", "33", "51", "52", "53", "70", "81",
                    "82", "83", "84", "85", "86", "87", "88", "90", "100"]
        for i in aph_list:
            data["aph"+str(i)] = {"WithSign": '', "WithOutSign": '', "WithSign_url": "", "WithOutSign_url": ""}
            url_sign = self.url.replace("aph", 'aph' + str(i))
            headers_sign['path'] = self.headers['path'].replace("aph", 'aph' + str(i))
            headers = headers_sign
            url = url_sign.replace("-sign", '')
            headers['path'] = self.headers['path'].replace("-sign", '')
            print(url, url_sign)
            req_sign = requests.get(url=url_sign, headers=headers_sign, stream=True)  #  请求待加固的包
            req = requests.get(url=url, headers=headers, stream=True)  # 请求不带加固的包
            # stream字段控制只下载respone头，不下载文件内容
            if req_sign.status_code == 200:
                size_sign = round(float(req_sign.headers['Content-length']) / 1024 / 1024, 2)
                data["aph" + str(i)]['WithSign'] = str(size_sign) + "MB"
                data["aph" + str(i)]['WithSign_url'] = url_sign
            else:
                data["aph" + str(i)]['WithSign'] = str(0) + "MB"
                data["aph" + str(i)]['WithSign_url'] = url_sign
            if req.status_code == 200:
                size = round(float(req.headers['Content-length']) / 1024 / 1024, 2)
                data["aph" + str(i)]['WithOutSign'] = str(size) + "MB"
                data["aph" + str(i)]['WithOutSign_url'] = url
            else:
                data["aph" + str(i)]['WithOutSign'] = str(0) + "MB"
                data["aph" + str(i)]['WithOutSign_url'] = url
        print(data)
        self.sendActionCard(data)

#
# if __name__ == '__main__':
#     a = writeForMeiQi("5.4.4", "2312")

# sudo ssh 120.55.97.27
# 输入你的电脑密码
# 输入：jnq19990520.
# 输入：python3 /pythonTest/WriteForMeiQi.py "5.4.4"  "2312"