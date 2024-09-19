import json


agentid = 1000002  # 应用id

def pushtemp(huse):
    payurl = 'http://www.sample.cn:/'
    weekchs=('周一','周二','周三','周四','周五','周六','周日',)
    if huse.costFlag:
        symbol = '-'
    if huse.rechargeFlag:
        symbol = '+'
    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
    data = {
        "touser": "@all",
        "msgtype": "template_card",
        "agentid": agentid,
        "template_card": {
            "card_type": "text_notice",
            "task_id": "task_id",
            "main_title": {
                "title": "昨日记账日报",
                "desc": f'{huse.listentime.month}月{huse.listentime.day}日({weekchs[huse.listentime.weekday()]})日报'
            },
            "horizontal_content_list": [
                {
                    "keyname": "昨日消费",
                    "value": f'￥{round(huse.today_cost,2)}'
                },
                {
                    "keyname": "昨日充值",
                    "value": f'￥{round(huse.today_recharge,2)}'
                },
                {
                    "keyname": "本月统计",
                    "value": f'{huse.yesterday.month}月已消费￥{round(huse.month_cost,2)}，已充值￥{round(huse.month_recharge,2)}'
                },
            ],
            "jump_list": [
                {
                    "type": 1,
                    "title": "E码通",
                    "url": payurl
                }
            ],
            "card_action": {
                "type": 1,
                "url": payurl
            }
        },
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    data = json.dumps(data)
    return data, url
