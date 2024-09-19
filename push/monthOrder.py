import json


agentid = 1000002  # 应用id

def pushtemp(huse):
    payurl = 'http://www.sample.cn/' #卡片中跳转url
    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
    data = {
        "touser": "@all",
        "msgtype": "template_card",
        "agentid": agentid,
        "template_card": {
            "card_type": "text_notice",
            "task_id": "task_id",
            "main_title": {
                "title": "上月记账月报",
                "desc": f'{huse.yesterday.month}月份月报'
            },
            "horizontal_content_list": [
                {
                    "keyname": "上月消费",
                    "value": f'￥{round(huse.month_cost,2)}'
                },
                {
                    "keyname": "上月充值",
                    "value": f'￥{round(huse.month_recharge,2)}'
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
