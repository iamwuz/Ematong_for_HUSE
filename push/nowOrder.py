import json

agentid = 1000002  # 应用id


def pushtemp(huse):
    if huse.costFlag:
        symbol = '-'
    if huse.rechargeFlag:
        symbol = '+'
    payurl = 'http://www.wuzspace.cn:8001/'
    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
    data = {
        "touser": "@all",
        "msgtype": "template_card",
        "agentid": agentid,
        "template_card": {
            "card_type": "text_notice",
            "task_id": "task_id",
            "main_title": {
                "title": "校园卡动账通知",
                "desc": huse.stuname + "同学，你有一笔新的交易"
            },

            "emphasis_content": {
                "desc": "交易金额",
                "title": symbol + "￥" + str(huse.orderMoney)
            },
            "quote_area": {
                "type": 0,
                "quote_text":huse.quote,
            },
            "horizontal_content_list": [
                {
                    "keyname": "交易类型",
                    "value": huse.orderType
                },
                {
                    "keyname": "支付方式",
                    "value": huse.summary
                },
                {
                    "keyname": "交易名称",
                    "value": huse.orderName
                },
                {
                    "keyname": "交易时间",
                    "value": huse.orderTime
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
