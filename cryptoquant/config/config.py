"""
web:  studyquant.com
author: Rudy
wechat:82789754
"""
import os

current_path = os.path.dirname(os.path.abspath(__file__))

if "privateconfig.py" in os.listdir(current_path):
    binance_api_key = ""
    binance_secret_key = ""
    from cryptoquant.config.privateconfig import *
    g_api_key = binance_api_key
    g_secret_key = binance_secret_key
else:
    # please input your binance api key and secret_key
    g_api_key = ""          #Common API KEY
    g_secret_key = ""
    # please input your binance api key and secret_key
    binance_api_key = ''
    binance_secret_key = ''

ok_api_key = ""
ok_seceret_key = ""
ok_passphrase = ""
test =1