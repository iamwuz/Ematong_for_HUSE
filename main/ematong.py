import json
import time
import requests
from datetime import datetime, timedelta
import sys
import os
import calendar

from flask import jsonify

"""import nowOrder
import todayOrder
import monthOrder
import workBench"""
# 将项目根目录添加到 sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 将项目根目录添加到 sys.path 中
sys.path.append(project_root)
from push import init, nowOrder, todayOrder, monthOrder, workBench, setAppMenu

info = None


class Husepaypush:
    def __init__(self):
        self.url = 'http://172.19.1.217:30110'
        #self.url = 'http://huseyktopen.huse.edu.cn:30110'
        # 个人信息
        self.user_name = '' #智校乐账号
        self.user_pwd = '' #智校乐密码
        self.dormitory = '' #智校乐宿舍号
        # 统计数据
        self.today_cost = 0.
        self.today_costNum = 0
        self.today_recharge = 0.
        self.today_rechargeNum = 0
        self.month_cost = 0.
        self.month_recharge = 0.
        self.today_electric = 0.
        self.balance = 0.
        self.monthFlag = False
        self.elecBalance = 0.
        self.nextDay = False
        self.summary = None
        # 订单信息
        self.orderMoney = 'null'
        self.orderType = 'null'
        self.orderTime = 'null'
        self.orderName = 'null'

    # 获取access_token
    def getAT(self):
        global info
        url = 'https://apppro.zhixiaole.net/v2/user/login?user_name=%s&user_pwd=%s' % (self.user_name, self.user_pwd)
        response = requests.post(url,headers={'Connection':'close'})
        data = json.loads(response.text)
        self.user_id = str(data['data']['id'])  # 用户id
        self.access_token = data['data']['access_token']  # ack
        self.vcard_no = data['data']['vcard_no']  # 虚拟卡账号
        self.school_id = str(data['data']['school_id'])  # 学校id
        info_dict = {'access_token': self.access_token}
        with open("../config/info.json", "w") as f:
            json.dump(info_dict, f)

    # 获取user_token
    def getUT(self):
        url = 'https://new.zhixiaole.net/third-party-api/xkpv8/h5/redirect?version=1.7.5&school_id=%s&user_id=%s&token=%s' % (
            self.school_id, self.user_id, self.access_token)
        response = requests.get(url,headers={'Connection':'close'})
        if response.text.find('鉴权失败') != -1 or response.status_code == 502:  # ack过期的情况
            self.getAT()
            self.getUT()
        else:
            try:
                list_response = response.history  # 获取重定向记录
                tid = list_response[len(list_response) - 1].headers.get('location')
            except IndexError as e:
                print(f'list_response: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  {e}')
                print(len(list_response))
                for i in range(len(list_response)):
                    print(f'第{i + 1}条 {list_response[i].headers}')
                print(f'getuk reloading~')
                self.getUT()
            index = tid.find('?tid')
            tid = tid[index + 5:]
            # 使用tid构造body获取uk
            body = {"tid": tid}
            response = requests.post(self.url + '/server/auth/getToken', json=body,headers={'Connection':'close'})
            data = json.loads(response.text)
            if data['success']:
                self.user_token = data['resultData']['accessToken']
            else:
                self.getUT()

    # 获取此刻订单数据
    def getnowOrder(self):
        Date = self.now.strftime('%Y-%m-%d')
        headers = {'Authorization': self.user_token}
        for i in range(1, 3):
            body = {
                "pageSize": "500",
                "tradeType": i,  # 消费
                "fromDate": Date,
                "toDate": Date,
            }
            while True:
                try:
                    response = requests.post(self.url + '/server/user/tradeList', json=body, headers=headers, timeout=10)
                except Exception as e:
                    print(f'getnoworder response {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  {e}')
                else:
                    break;
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + str(response.status_code))
            if response.status_code != 200:
                self.getUT()
                self.getnowOrder()
            else:
                while True:
                    try:
                        data = json.loads(response.text)
                        break
                    except json.decoder.JSONDecodeError as e:
                        print(f'getnoworder jsonloader {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  {e}')
                        response = requests.post(self.url + '/server/user/tradeList', json=body, headers=headers, timeout=10)
                        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + str(response.status_code))
                        if response.status_code != 200:#多半是ut过期了
                            self.getUT()
                            response = requests.post(self.url + '/server/user/tradeList', json=body, headers=headers,
                                                     timeout=10)
                if data['success']:
                    new_costNum = len(data['resultData'])
                    if i == 1:
                        if self.today_costNum < new_costNum:  # 如果有新订单
                            for item in range(0, new_costNum - self.today_costNum):  # 理论上同一时刻只有一条新订单
                                self.orderTime = data['resultData'][item]['date']
                                self.orderMoney = abs(float(data['resultData'][item]['amt']))
                                self.orderType = '消费'
                                summary = data['resultData'][item]['summary']
                                self.summary = '微信-POS扫码' if '微信' in summary else '支付宝-POS扫码' if '支付宝' in summary else '虚拟卡'
                                self.orderName = data['resultData'][item]['merchantName']
                                self.today_cost += abs(float(data['resultData'][item]['amt']))  # 加上最新的一条
                                if self.monthFlag:
                                    self.month_cost += abs(float(data['resultData'][item]['amt']))
                            self.today_costNum = new_costNum
                            self.costFlag = True
                        else:
                            self.costFlag = False
                    else:
                        if self.today_rechargeNum < new_costNum:
                            for item in range(0, new_costNum - self.today_rechargeNum):
                                self.orderTime = data['resultData'][item]['date']
                                self.orderMoney = data['resultData'][item]['amt']
                                self.orderType = '充值'
                                self.summary = '工行卡（8860）'
                                self.orderName = data['resultData'][item]['merchantName']
                                self.today_recharge += abs(float(data['resultData'][item]['amt']))
                                if self.monthFlag:
                                    self.month_recharge += abs(float(data['resultData'][item]['amt']))
                            self.today_rechargeNum = new_costNum
                            self.rechargeFlag = True
                        else:
                            self.rechargeFlag = False
                else:
                    self.getUK()

    # 获取本月订单数据
    def getMonthOrder(self):  # 可以用于初始化和校准月数据
        self.monthFlag = True  # 有新订单才需要计算本月，否则monthflag为false
        start_Date = self.now.strftime('%Y-%m-01')
        end_Date = self.now.strftime('%Y-%m-%d')
        headers = {'Authorization': self.user_token}
        for i in range(1, 3):
            body = {
                "pageSize": "500",
                "tradeType": i,  # tradeType:1消费 2充值
                "fromDate": start_Date,
                "toDate": end_Date,
            }
            response = requests.post(self.url + '/server/user/tradeList', json=body, headers=headers)
            if response.status_code == 401:
                self.getUT()
                self.getMonthOrder()
            else:
                data = json.loads(response.text)
                if data['success']:
                    new_costNum = len(data['resultData'])
                    if i == 1:
                        for item in range(0, new_costNum):
                            self.month_cost += abs(float(data['resultData'][item]['amt']))
                    else:
                        for item in range(0, new_costNum):
                            self.month_recharge += abs(float(data['resultData'][item]['amt']))

    def getElectric(self):
        headers = {'Authorization': self.user_token}
        body = {
            "utilityType": "electric",
            "room": self.dormitory
        }
        while True:
            try:
                resp = requests.post(self.url + '/server/utilities/account', headers=headers, json=body)
                data = json.loads(resp.text)
            except json.decoder.JSONDecodeError as e:
                    self.getUT()
                    print(f'getelectric ut outdate:  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {e}')
            except Exception as e:
                    print(f'getelectric response&json:  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {e}')
            else:
                break
        if data['success']:
            while True:
                try:
                    for i in range(0,len(data['resultData']['templateList'])):
                        if(data['resultData']['templateList'][i]['code']=='quantity'):
                            break
                    if self.elecBalance != int(float(data['resultData']['templateList'][i]['value']) * 100) / 100.0:
                        self.elecFlag = True
                    else:
                        self.elecFlag = False
                    self.elecBalance = int(float(data['resultData']['templateList'][i]['value']) * 100) / 100.0
                    self.balance = int(float(data['resultData']['balance']) * 100) / 100.0
                    self.stuname = data['resultData']['utilityUsername']
                except Exception as e:
                    print(f'getelectric data  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  {e}')
                    print(data)
                else:
                    break
            self.quote = ''
            if self.balance < 15:
                self.quote='提醒：校园卡余额告急，请及时充值~'
            if self.elecBalance < 15:
                if self.quote=='':
                    self.quote='提醒：宿舍电量告急，请及时充值~'
                else:
                    self.quote+='\n　　　宿舍电量告急，请及时充值~'
        else:
            self.getUT()  # 更新uk
            self.getElectric()

    def sendMessage(self, ordertype):
        data = None
        url = None
        if ordertype == 'now':
            data, url = nowOrder.pushtemp(self)
        elif ordertype == 'today':
            data, url = todayOrder.pushtemp(self)
        elif ordertype == 'month':
            data, url = monthOrder.pushtemp(self)
        elif ordertype == 'workbench':
            data, url = workBench.worktemp(self)
        elif ordertype == 'menu':
            data, url = setAppMenu.setMenu(self)
        resp = requests.post(url=url + self.push_access_token, data=data)
        print(ordertype+' '+resp.text)

    def initInfo(self):
        self.getAT()
        self.getUT()
        self.getnowOrder()
        self.getElectric()
        self.getMonthOrder()

    def listenOrder(self):
        self.getnowOrder()
        self.getElectric()

    def cleanData(self):
        self.now = datetime.now()
        self.yesterday = self.now - timedelta(days=1)
        ldom = calendar.monthrange(self.listentime.year, self.listentime.month)[1] #last_day_of_month

        if self.now.day%ldom > self.listentime.day%ldom:  # 每日数据
            self.sendMessage('today') #发送昨日数据
            self.listentime = self.now
            self.today_cost = 0
            self.today_recharge = 0
            self.today_costNum = 0
            self.today_rechargeNum = 0
            self.rechargeFlag = False
            self.costFlag = False
            self.nextDay = True
            print(f'{self.listentime}  cleanData~~~')
            self.sendMessage('workbench')

        if self.now.month > self.yesterday.month and self.nextDay:  # 月数据
            self.sendMessage('month') #发送上月数据
            self.month_cost = 0
            self.month_recharge = 0
            self.nextDay = False
        

    def checkpushToken(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/getcallbackip?access_token=' + self.push_access_token
        resp = requests.get(url).json()
        if resp['errcode'] == 42001:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' qywxToken过期~')
            self.push_access_token=init.getAT(huse)
            self.checkpushToken()



if __name__ == '__main__':
    huse = Husepaypush()
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' start')
    huse.push_access_token = init.getAT(huse)  # 获取推送access_token并设置requireATtime
    huse.sendMessage('menu')
    huse.listentime = datetime.now()
    huse.cleanData()  # 按天按月重置数据
    huse.initInfo()
    workBench.worktempinit(huse)
    huse.sendMessage(ordertype='workbench')
    while True:
        huse.checkpushToken()
        huse.listenOrder()  # 监听订单
        if huse.costFlag or huse.rechargeFlag:  # 如果有新订单则推送消息
            huse.sendMessage('now')
            huse.sendMessage('workbench')
        if huse.elecFlag:
            huse.sendMessage('workbench')
        huse.cleanData()  # 按天按月重置数据
        time.sleep(3)
