# An Quantatitive trading library for crypto-assets 数字货币量化交易框架

<p align="center">
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.6-blue.svg"/>
    <img src ="https://img.shields.io/badge/python-3.7-blue.svg"/>
</p>

# cryptoquant
CryptoQuant is an algorithmic trading library for crypto-assets written in Python. It allows trading strategies to be easily expressed and backtested against historical data (with daily and minute resolution), providing analytics and insights regarding a particular strategy's performance. cryptoquant also supportslive-trading of crypto-assets starting with many exchanges (Okex,Binance,Bitmex etc) with more being added over time.

CryptoQuant是一套基于Python的量化交易框架，帮助个人/机构量化人员进行数字货币量化交易。框架具有回测/实盘交易功能。 策略框架支持多个平台切换回测。 并提供交易所实盘交易接口（如OKEX) 。

全新的《Python数字货币量化投资实战》系列在线课程，已经在微信公众号[**StudyQuant**]上线，一整套数字货币量化解决方案。覆盖CTA等策略（已完成）等内容。



## Features
- Ease of Use: CryptoQuant tries to get out of your way so that you can focus on algorithm development. 
- **开箱即用 ** ： CryptoQuant提供一套量化框架帮助您专注策略开发
- **回测**：回测框架支持数据导入，自定义交易订单号，多线程回测、遗传算法寻优等功能
- **实盘交易**： 框架提供数字货币交易所接口DEMO
- **文档支持**:[**官方社区论坛**](https://docs.studyquant.com/)

## 环境准备
* 支持的系统版本：Windows 7以上/Windows Server 2008以上/Ubuntu 18.04 LTS
* 支持的Python版本：Python 3.6 64位/ 3.7+ 
## Installation

**Windows**
使用要安装Python，激活环境，进入cryptoquant/install目录下的运行install.bat 安装依赖库
安装dependencies 中的依赖库

## Quickstart

### 如何导入数据

```Python
from cryptoquant.trader.constant import Direction, Exchange, Interval, Offset, Status, Product, OptionType, OrderType
import pandas as pd
from cryptoquant.app.data_manage.data_manager import save_data_to_cryptoquant

if __name__ == '__main__':
    df = pd.read_csv('IF9999.csv')
    symbol = 'IF9999'
    save_data_to_cryptoquant(symbol, df, Exchange.CFFEX)
    
```

### 如何回测
```Python
from datetime import datetime
from cryptoquant.app.cta_backtester.engine import BacktestingEngine, OptimizationSetting
from cryptoquant.app.cta_strategy.strategies.atr_rsi_strategy import (
    AtrRsiStrategy,
)
#%%
engine = BacktestingEngine()

engine.set_parameters(
    vt_symbol="IF9999.CFFEX",
    interval="1m",
    start=datetime(2020, 1, 1),
    end=datetime(2020, 4, 30),
    rate=0.3/10000,
    slippage=0.5,
    size=300,
    pricetick=0.2,
    capital=1_000_0,
)
setting = {}
engine.add_strategy(AtrRsiStrategy,setting)
# 导入数据
engine.load_data()
# 开始回测
engine.run_backtesting()
#计算收益
df = engine.calculate_result()
# 开始统计
engine.calculate_statistics()
# 开始画图
engine.show_chart()
```


```Python
from cryptoquant.trader.constant import Direction, Exchange, Interval, Offset, Status, Product, OptionType, OrderType
import pandas as pd
from cryptoquant.app.data_manage.data_manager import save_data_to_cryptoquant

if __name__ == '__main__':
    df = pd.read_csv('IF9999.csv')
    symbol = 'IF9999'
    save_data_to_cryptoquant(symbol, df, Exchange.CFFEX)
    
```

### 实盘交易
```Python
from cryptoquant.api.okex.okex_spot_exchange import OkexSpotApi
#导入交易所接口密钥
from cryptoquant.config.config import ok_api_key, ok_seceret_key, ok_passphrase
from cryptoquant.api.okex.spot_api import SpotAPI
from cryptoquant.api.api_gateway.apigateway import ApiGateway

# 实例化OKEX接口的类
api = SpotAPI(ok_api_key, ok_seceret_key, ok_passphrase, True)
# 实例化自己封装好接口类
api_gateway = OkexSpotApi(api)
# 实例化策略与交易所接口之间的中间通道类
exchange = ApiGateway(api_gateway)
kline_df = exchange.get_kline_data(symbol, minutes)
print(kline_df)
ticker = exchange.get_ticker(symbol)
print(ticker)

# 买单
order_data = exchange.buy(symbol,3,1)
# 卖单
# order_data = exchange.sell(symbol, 6, 1)


```
## 捐助
如果您觉得我们的开源软件对你有所帮助，请扫下方二维码购买课程支持。

<p align="center">
    <img src ="https://images.gitee.com/uploads/images/2021/0115/114257_f54ef081_5152232.png"/>
</p>


## Questions?
- QQ社群：1032965883
如果无法解决请前往[**官方社区论坛**](https://docs.studyquant.com/)的


## 贡献代码

非常希望大牛来贡献代码，完善项目功能。 

在提交代码的时候，请遵守以下规则，以提高代码质量：
  * 使用[autopep8](https://github.com/hhatto/autopep8)格式化你的代码。运行```autopep8 --in-place --recursive . ```即可。
  * 使用[flake8](https://pypi.org/project/flake8/)检查你的代码，确保没有error和warning。在项目根目录下运行```flake8```即可。



## 开发日志

2021-01-15    v1.1

- 添加了APIGATEWAY 模板

- 添加了实盘交易DEMO

- 完善了回测框架



2020-08-15    v1.0

- 开源框架