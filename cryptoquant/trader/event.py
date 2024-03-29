"""
Event type string used in VN Trader.
"""

from cryptoquant.event import EVENT_TIMER  # noqa
EVENT_GET_TICK = "get_eTick."
EVENT_TICK = "eTick."
EVENT_TRADE = "eTrade."
EVENT_ORDER = "eOrder."
EVENT_POSITION = "ePosition."
EVENT_ACCOUNT = "eAccount."
EVENT_CONTRACT = "eContract."
EVENT_LOG = "eLog"
EVENT_OPEN_ORDER = "eOpenorder"
EVENT_KLINE = "eKline"
CRYPTO_EVENT_ACCOUNT = "crypto_eAccount."
STRATEGY_EVENT = "crypto_strategy_handle."