# 通过接口给用户发送应用内消息

import requests
import json
import time


global user_id, channel_id, comment_id, video_id, message_id
user_id = "7952734"
channel_id = ""
comment_id = "5ecf73ec97921904d1a1ac0f"
video_id = "ccm-jehbsp9pa0"
message_id = ""

remindType = {
    "remind_top_asset": {"jump_value": None, "subtitle": "测试提现消息副标题", "title": "测试提现消息标题",
                         "user_id": user_id, "guide_word": "去提现", "tip_word": "资产新增"},
    "remind_top_seed": {"jump_value": None, "subtitle": "测试南瓜籽消息副标题", "title": "测试南瓜籽消息标题",
                         "user_id": user_id, "guide_word": "查看", "tip_word": "南瓜籽新增"},
    "remind_top_live_change": {"jump_value": {"channel_id": channel_id},
                        "subtitle": "测试放映厅换片消息副标题", "title": "测试放映厅换片消息标题",
                        "user_id": user_id, "guide_word": "去换片", "tip_word": "放映厅换片"},
    "remind_top_live_gift": {"jump_value": {"channel_id": channel_id}, "subtitle": "测试收到礼物消息副标题", "title": "测试收到礼物消息标题",
                         "user_id": user_id, "guide_word": "感谢他", "tip_word": "放映厅收到礼物"},
    "remind_top_live_lottery": {"jump_value": {"channel_id": channel_id, "lottery_id": "jiangnanqianghaoshuai"},
                                "subtitle": "测试抽奖消息副标题", "title": "测试抽奖消息标题",
                         "user_id": user_id, "guide_word": "查看", "tip_word": "放映厅抽奖"},
    "remind_top_live_open": {"jump_value": {"user_id": user_id, "channel_id": channel_id},
                             "subtitle": "测试开厅消息副标题", "title": "测试开厅消息标题",
                         "user_id": user_id, "guide_word": "去捧场", "tip_word": "关注的人开厅"},
    "remind_top_message": {"jump_value":  {"user_id": user_id, "user_nickname": "芋圆啵啵奶茶"},
                         "subtitle": "测试私信消息副标题", "title": "测试私信消息标题",
                         "user_id": user_id, "guide_word": "回复", "tip_word": "私信通话"},
    "remind_top_comment_reply": {"jump_value": {"comment_id": comment_id},
                                 "subtitle": "测试影评消息副标题", "title": "测试影评消息标题",
                         "user_id": user_id, "guide_word": "查看", "tip_word": "影评评论及回复"},
    "remind_top_comment_like": {"jump_value": {"comment_id": comment_id},
                         "subtitle": "测试影评点赞消息副标题", "title": "测试影评点赞消息标题",
                         "user_id": user_id, "guide_word": "查看", "tip_word": "影评及影评评论被点赞"},
    "remind_top_commentary_reply": {"jump_value": {"video_id": video_id, "comment_id": None,"reply_id": None},
                        "subtitle": "测试解说消息副标题", "title": "测试解说消息标题",
                        "user_id": user_id, "guide_word": "查看", "tip_word": "解说的评论回复"},
    "remind_top_commentary_like": {"jump_value": {"video_id": video_id, "comment_id": None, "reply_id": None},
                                "subtitle": "测试解说点赞消息副标题", "title": "测试解说点赞消息标题",
                                "user_id": user_id, "guide_word": "查看", "tip_word": "解说评论或回复被点赞"},
    "remind_top_fans": {"jump_value": {"other_user_id": "4017434"},
                        "subtitle": "测试新增粉丝消息副标题", "title": "测试新增粉丝消息标题",
                        "user_id": user_id, "guide_word": "看看他", "tip_word": "新增粉丝"},
    "remind_top_customer": {"jump_value": None, "subtitle": "测试客服消息副标题", "title": "测试客服消息标题",
                        "user_id": user_id, "guide_word": "查看", "tip_word": "客服消息"},
    "remind_top_system_message": {"jump_value": {"message_id": message_id}, "subtitle": "测试系统消息副标题", "title": "测试系统消息标题",
                        "user_id": user_id, "guide_word": "查看", "tip_word": "系统消息"},
}


def makeRemindData(remindtype):
    if remindtype not in remindType.keys():
        remind = remindType["remind_top_customer"]
    else:
        remind = remindType[remindtype]
    data = {
        "jump_value": remind["jump_value"],  # json 对象 消息参数
        "subtitle": "蒋南强觉得有必要看下这个提示语会不会超长" + remind["subtitle"],  # 副标题
        "title": "蒋南强觉得有必要看下这个提示语会不会超长" + remind["title"],  # 标题
        "type": str(remindtype),  # 消息类型
        "user_id": remind["user_id"],  # 用户编号
        "guide_word": "蒋南强觉得有必要看下这个提示语会不会超长" + remind["guide_word"],  # 引导词
        "tip_word": "蒋南强觉得有必要看下这个提示语会不会超长" + remind["tip_word"]  # 提示语
    }
    return data


def sendRemind(env, remindtype):
    remindtype = remindtype
    if env.lower() == "dev":
        url = "https://dev-environmental.vcinema.cn:4100/remind/top"
    elif env.lower() == "online":
        url = "http://172.17.63.245:4100/remind/top"
    else:
        url = "https://dev-environmental.vcinema.cn:4100/remind/top"
    headers = {
        "content-type": "application/json"
    }
    data = makeRemindData(remindtype)
    req = requests.post(url=url, headers=headers, data=json.dumps(data))
    print(req.text)


# demmo 以下是demmo

for i in remindType.keys():
    sendRemind("env", str(i))
    time.sleep(1)


