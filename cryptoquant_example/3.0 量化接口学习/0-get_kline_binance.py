"""
=========================================================
* Powered by Rudy
* author: Rudy
* wechat: 
=========================================================
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
"""
import pandas as pd
import numpy as np

"""
    1. http和requests讲解

    1. http是Hyper Text Transfer Protocal (超文本传输协议)
        有如下特点：
        1. 简单快速：客户端向服务器请求时，只需要传递方法和路径。常用的请求方法有GET, POST, DELET等方法
        2. 灵活： 可以传递任意类型的数据对象， 文件、字符串等
        3. 无状态： Http协议是无状态协议，对请求的事务处理没有记忆能力，如果后续处理需要前面的信息，则需要重传。

    2. http协议URL
        1. 协议部分： 以http或者https开头
        2. 域名部分： 主机地址
        3. 端口号： 默认使用80端口，如果非80端口，需要指明端口号
        4. 虚拟目录部分
        5. 参数部分？
        6. 其他(文件部分， 锚部分)
        
    3. http请求和相应
        客户端发送一个请求到服务器包含以下内容：
            1. 请求行（用来说明请求类型，所使用的http版本）
            2. 请求头header（User-Agent, Accept-Encoding、Referer等）
            3. 空行
            4. 请求数据
        一般情况下，服务器接收到数据请求后，会返回一个相应的信息
            1. 状态码 200(ok,请求成功)， 3xx(重定向) ，400(Bad Request)， 403(Forbidden请求被拒绝) 404 Not Found(资源不存在)
               500（internal server Error 服务器发生错误 503 Server Unavailable(服务器器不能处理请求。)
            2. 消息头 生成响应的时间、 指定相应的内容Content-Type等
            3. 空行
            4. 相应的正文
    Python中请求的框架， requests, aiohttp

"""

import requests
from requests import Response
import pandas as pd
import time

url1 = 'https://api.binance.com/api/v3/klines'
params = {'symbol': 'BTCUSDT', 'interval': '1m', 'limit': 100}
data: Response = requests.get(url1, params=params, timeout=5)

# data: Response  = requests.get(url, timeout=5)
print(data.status_code)
print(data.headers)
data2 = data.json()

#2021-01-01至 2021-12-31

df = pd.DataFrame(data2, columns=['begin_time', 'open', 'high', 'low', 'close', 'volume', 'end_time', 'turnover',
                                  'trades_number',
                                  'active_buy_volume',
                                  'active_buy_turnover',
                                  'ignore_parms'
                                  ])

df['begin_time'] = df['begin_time'] / (10 ** 3)
df['end_time'] = df['end_time'] / (10 ** 3)

df.loc[:, 'begin_time_str'] = df['begin_time'].apply(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x)))
df.loc[:, 'end_time_str'] = df['end_time'].apply(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x)))
df['time'] = df['begin_time_str']
df.index = df['time']
final = pd.DataFrame(df[['open', 'high', 'low', 'close', 'volume']], dtype=float)
final.index = df.index
kline = final[['open', 'high', 'low', 'close', 'volume']]

print(kline)
