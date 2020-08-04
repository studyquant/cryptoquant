# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         dingding
# Description:  
# Author:       Rudy
# U:            project
# Date:         2020-05-20
#-------------------------------------------------------------------------------

"""
StudyQuant:项目制的量化投资学院，帮你快速入行量化交易。
wechat:82789754
"""


import json
import requests

def sendmessage(url,message,keywords = None):
    #钉钉机器人的webhook地址
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    # keywords = '提示'
    message = str(message) + str(keywords)
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": str(message)},
#         "at": {
##            "atMobiles": [
##                "130xxxxxxxx"                                    #如果需要@某人，这里写他的手机号
##            ],
#            "isAtAll": 1                                        #如果需要@所有人，这些写1
#        }
    }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)

   # 签名
    # import time
    # import hmac
    # import hashlib
    # import base64
    # import urllib.parse
    #
    # timestamp = str(round(time.time() * 1000))
    # secret = 'this is secret'
    # secret_enc = secret.encode('utf-8')
    # string_to_sign = '{}\n{}'.format(timestamp, secret)
    # string_to_sign_enc = string_to_sign.encode('utf-8')
    # hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    # sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # print(timestamp)
    # print(sign)

if __name__=="__main__":
    # url1 = 'https://oapi.dingtalk.com/robot/send?access_token='
    url = 'https://oapi.dingtalk.com/robot/send?access_token='
    url1 = 'https://oapi.dingtalk.com/robot/send?access_token='

    content = '开空:BTCUSDT amount: (0.001) @ price:9766.0, 订单类型:限价'
    sendmessage(url,content,keywords= '提示')
    sendmessage(url1,content)

    
    
"""
好好学习，天天向上。 
project
"""