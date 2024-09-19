import json

agentid = 1000002 #应用id
#工作台模板初始化
def worktempinit(huse):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/agent/set_workbench_template?access_token='
    data = {
        "agentid": agentid,
        "type": "keydata",
        "replace_user_data": True
    }
    data = json.dumps(data)
    return data, url

#工作台模板数据
def worktemp(huse):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/agent/set_workbench_data?access_token='
    data = {
        "agentid": agentid,
        "userid": "WuZhiQiang",
        "type": "keydata",
        "keydata": {
            "items": [
                {
                    "key": "今日消费",
                    "data": str(round(huse.today_cost, 2)),
                },
                {
                    "key": "卡内余额",
                    "data": str(round(huse.balance, 2)),
                },
                {
                    "key": "剩余电量",
                    "data": str(round(huse.elecBalance,2)),
                }
            ]
        }
    }
    data = json.dumps(data)
    return data, url
