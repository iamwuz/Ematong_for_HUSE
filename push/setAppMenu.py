import json

agentid = 1000002  # 应用id


def setMenu(huse):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/menu/create?agentid=' + str(agentid) + '&access_token='
    data = {
        "button": [
            {
                "type": "view",
                "name": "E码通",
                "url": "http://hn1-lcf.luochancy.com:61600/"
            },
            {
                "type": "view",
                "name": "宿舍电费",
                "url": "http://hn1-lcf.luochancy.com:61600/"
            },
            {
                "name": "数据统计",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "今日数据",
                        "key": "V1001_GOOD"
                    },
                    {
                        "type": "click",
                        "name": "本月数据",
                        "key": "V1001_GOOD"
                    },
                ]
            }
        ]
    }
    data = json.dumps(data)
    return data, url
