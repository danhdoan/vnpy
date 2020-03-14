"""
General constant string used in VN Trader.
"""

from enum import Enum


class Direction(Enum):
    """
    Direction of order/trade/position.
    """
    # BRIAN: 多 - Long
    LONG = "Long"
    # BRIAN: 空 - Short
    SHORT = "Short"
    # BRIAN: 净 - Net
    NET = "Net"


class Offset(Enum):
    """
    Offset of order/trade.
    """
    NONE = ""
    # BRIAN: 开 - Open
    OPEN = "Open"
    # BRIAN: 平 - Close
    CLOSE = "Close"
    # BRIAN: 平今 - Close Today
    CLOSETODAY = "Close Today"
    # BRIAN: 平昨 - Close Yesterday
    CLOSEYESTERDAY = "Close Yesterday"


class Status(Enum):
    """
    Order status.
    """
    # BRIAN: 提交中 - Submitting
    SUBMITTING = "Submitting"
    # BRIAN: 未成交 - Not Traded
    NOTTRADED = "Not Traded"
    # BRIAN: 部分成交 - Part Traded
    PARTTRADED = "Part Traded"
    # BRIAN: 全部成交 - All Traded
    ALLTRADED = "All Traded"
    # BRIAN: 已撤销 - Canceled
    CANCELLED = "Canceled"
    # BRIAN: 拒单 - Rejected
    REJECTED = "Rejected"


class Product(Enum):
    """
    Product class.
    """
    # BRIAN: 股票 - Equity
    EQUITY = "Equity"
    # BRIAN: 期货 - Futures
    FUTURES = "Futures"
    # BRIAN: 期权 - Option
    OPTION = "Option"
    # BRIAN: 指数 - Index
    INDEX = "Index"
    # BRIAN: 外汇 - Forex
    FOREX = "Forex"
    # BRIAN: 现货 - Spot
    SPOT = "Spot"
    
    ETF = "ETF"
    # BRIAN: 债券 - Bond
    BOND = "Bond"
    # BRIAN: 权证 - Warrant
    WARRANT = "Warrant"
    # BRIAN: 价差 - Spread
    SPREAD = "Spread"
    # BRIAN: 基金 - Fund
    FUND = "Fund"


class OrderType(Enum):
    """
    Order type.
    """
    # BRIAN: 限价 - Limit
    LIMIT = "Limit"
    # BRIAN: 市价 - Market
    MARKET = "Market"
    STOP = "STOP"
    FAK = "FAK"
    FOK = "FOK"


class OptionType(Enum):
    """
    Option type.
    """
    # <TO_CONFIRM>
    # BRIAN: 看涨期权 - Call
    CALL = "Call"
    # BRIAN: 看跌期权 - Put
    PUT = "Put"


class Exchange(Enum):
    """
    Exchange.
    """
    # Chinese
    CFFEX = "CFFEX"         # China Financial Futures Exchange
    SHFE = "SHFE"           # Shanghai Futures Exchange
    CZCE = "CZCE"           # Zhengzhou Commodity Exchange
    DCE = "DCE"             # Dalian Commodity Exchange
    INE = "INE"             # Shanghai International Energy Exchange
    SSE = "SSE"             # Shanghai Stock Exchange
    SZSE = "SZSE"           # Shenzhen Stock Exchange
    SGE = "SGE"             # Shanghai Gold Exchange
    WXE = "WXE"             # Wuxi Steel Exchange

    # Global
    SMART = "SMART"         # Smart Router for US stocks
    NYMEX = "NYMEX"         # New York Mercantile Exchange
    COMEX = "COMEX"         # a division of theNew York Mercantile Exchange
    GLOBEX = "GLOBEX"       # Globex of CME
    IDEALPRO = "IDEALPRO"   # Forex ECN of Interactive Brokers
    CME = "CME"             # Chicago Mercantile Exchange
    ICE = "ICE"             # Intercontinental Exchange
    SEHK = "SEHK"           # Stock Exchange of Hong Kong
    HKFE = "HKFE"           # Hong Kong Futures Exchange
    HKSE = "HKSE"           # Hong Kong Stock Exchange
    SGX = "SGX"             # Singapore Global Exchange
    CBOT = "CBT"            # Chicago Board of Trade
    CBOE = "CBOE"           # Chicago Board Options Exchange
    CFE = "CFE"             # CBOE Futures Exchange
    DME = "DME"             # Dubai Mercantile Exchange
    EUREX = "EUX"           # Eurex Exchange
    APEX = "APEX"           # Asia Pacific Exchange
    LME = "LME"             # London Metal Exchange
    BMD = "BMD"             # Bursa Malaysia Derivatives
    TOCOM = "TOCOM"         # Tokyo Commodity Exchange
    EUNX = "EUNX"           # Euronext Exchange
    KRX = "KRX"             # Korean Exchange

    OANDA = "OANDA"         # oanda.com

    # CryptoCurrency
    BITMEX = "BITMEX"
    OKEX = "OKEX"
    HUOBI = "HUOBI"
    BITFINEX = "BITFINEX"
    BINANCE = "BINANCE"
    BYBIT = "BYBIT"         # bybit.com
    COINBASE = "COINBASE"
    DERIBIT = "DERIBIT"
    GATEIO = "GATEIO"
    BITSTAMP = "BITSTAMP"

    # Special Function
    LOCAL = "LOCAL"         # For local generated data


class Currency(Enum):
    """
    Currency.
    """
    USD = "USD"
    HKD = "HKD"
    CNY = "CNY"


class Interval(Enum):
    """
    Interval of bar data.
    """
    MINUTE = "1m"
    HOUR = "1h"
    DAILY = "d"
    WEEKLY = "w"
