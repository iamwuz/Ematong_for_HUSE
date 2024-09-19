import requests
from datetime import datetime, timedelta


# 获取推送通知access_token
def getAT(huse):
    corpid = 'ww9bb7df2a3f29e83b'  # 企业ID
    corpsecret = 'pXhUueoywiLGHo-D1bzGXJkEZEUxC76rNDTGcQ1j_J8'  # Secret
    #corpsecret = 'ehn2EvI1nFVN7iLlTWub6So1siXhWzQjSTmeepNbSmQ'
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (corpid, corpsecret)
    resp = requests.get(url).json()
    return resp['access_token']
