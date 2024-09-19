import requests
from datetime import datetime, timedelta


# 获取推送通知access_token
def getAT(huse):
    corpid = ''  # 企业ID
    corpsecret = ''  # Secret
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (corpid, corpsecret)
    resp = requests.get(url).json()
    return resp['access_token']
