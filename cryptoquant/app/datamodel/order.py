"""
=========================================================
* Powered by StudyQuant 
* author: Rudy
* wechat:studyquant88
=========================================================
* Product Page: https://studyquant.com
* Copyright 2021 StudyQuant
* License (https://studyquant.com/)
* Coded by https://studyquant.com
=========================================================
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
"""
from typing import Dict
from dataclasses import dataclass

@dataclass
class Order():
    Info: Dict
    Id: int = 0
    Status: int =0    # 订单状态，参考常量里的订单状态，例如：ORDER_STATE_CLOSED
    Type: int = 0     # 订单类型，参考常量里的订单类型，例如：ORDER_TYPE_BUY
    Offset: int = 0   # 开仓，还是平仓
    Price: float = 0
    Amount: float = 0
    DealAmount: float = 0
    AvgPrice: float = 0
    ContractType: str = ''
    #------ 用户习惯不同---------

    def __post_init__(self):
        """"""
        pass
        # self.Available_balance = self.Balance - self.FrozenBalance
        # self.Available_stocks = self.Stocks - self.FrozenStocks

        self.info = self.Info
        self.id = self.Id
        self.status = self.Status  # 订单状态，参考常量里的订单状态，例如：ORDER_STATE_CLOSED
        self.type = self.Type     # 订单类型，参考常量里的订单类型，例如：ORDER_TYPE_BUY
        self.direction = self.Offset
        # Offset = Direction
        self.price = self.Price
        self.amount = self.Amount
        self.deal_amount = self.DealAmount
        self.avg_price = self.AvgPrice
        self.contract_type = self.ContractType

        # info = Info
        # id = Id
        # status = Status  # 订单状态，参考常量里的订单状态，例如：ORDER_STATE_CLOSED
        # type = Type     # 订单类型，参考常量里的订单类型，例如：ORDER_TYPE_BUY
        # direction = Offset
        # # Offset = Direction
        # price = Price
        # amount = Amount
        # deal_amount = DealAmount
        # avg_price = AvgPrice
        # contract_type = ContractType

