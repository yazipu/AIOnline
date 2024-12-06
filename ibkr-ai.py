import yfinance as yf
from ib_insync import IB, Stock, MarketOrder
import ibapi
import importlib.metadata
from datetime import datetime, time as time1

import pandas as pd
import pandas_market_calendars as mcal
import pytz, time, random

# 定义标的和其交易参数（以金额为单位）
symbols = {
    # 'QQQ': { 'buy_value': 910, 'sell_value': 1050, 'trade_amount': 70 },
    'TQQQ': { 'buy_value': 980, 'trade_amount': 88, 'market': 'US' },
    'RKLB': { 'buy_value': 780, 'trade_amount': 39, 'market': 'US' },
    'GME': { 'buy_value': 480, 'trade_amount': 39, 'market': 'US' },
    'KODK': { 'buy_value': 480, 'trade_amount': 39, 'market': 'US' },
    'BEKE': { 'buy_value': 480, 'trade_amount': 39, 'market': 'US' },
    'INTC': { 'buy_value': 480, 'trade_amount': 39, 'market': 'US' },
}

# 设置不同市场的时区
eastern = pytz.timezone('America/New_York') # 纽约
hong_kong = pytz.timezone('Asia/Hong_Kong') # 香港
china = pytz.timezone('Asia/Shanghai')      # 中国

# 获取不同市场的交易日历
nyse = mcal.get_calendar('NYSE')    # 美股
hkex = mcal.get_calendar('HKEX')    # 港股

# 上海证券交易所日历，用于 A 股
cndata = mcal.get_calendar('XSHG')  # A股

def get_market_status(market):
    """
    检查指定股票在对应市场当前是否开盘
    :param market: 市场代码（'US' 表示美股市场，'HK' 表示港股市场，'CN' 表示 A 股市场）
    :return: True 如果市场开盘，False 如果未开盘
    """
    if market == 'US': calendar = nyse; timezone = eastern
    elif market == 'HK': calendar = hkex; timezone = hong_kong
    elif market == 'CN': calendar = cndata; timezone = china
    else: raise ValueError("市场代码无效，请使用 'US'、'HK' 或 'CN'")

    current_time = datetime.now(timezone)
    today = current_time.date()
    schedule = calendar.schedule(start_date=today, end_date=today)

    # 如果当天没有开放时间，则表示未开盘
    if schedule.empty: return False

    # 获取市场的开盘和收盘时间
    market_open = schedule.iloc[0]['market_open'].astimezone(timezone)
    market_close = schedule.iloc[0]['market_close'].astimezone(timezone)

    # 检查当前时间是否在开盘时间内
    if market == 'CN':
        # A 股有午间休市，需要分别检查上午和下午时段
        current_time_time = current_time.time()
        morning_open = time1(9, 30); morning_close = time1(11, 30); afternoon_open = time1(13, 0); afternoon_close = time1(15, 0)
        return ((morning_open <= current_time_time < morning_close) or (afternoon_open <= current_time_time < afternoon_close))
    else: return market_open <= current_time < market_close

# 获取 ib_insync 和 ibapi 的版本信息
ib_insync_version = importlib.metadata.version('ib_insync')
ib_api_version = ibapi.__version__ if hasattr(ibapi, '__version__') else "Unknown"

print("ib_insync 版本:", ib_insync_version)
print("IB API 版本:", ib_api_version)

# 连接到 IB Gateway（端口 4001）
ib = IB(); ib.connect('127.0.0.1', 4001, clientId=1)

def truncate(number, decimal_places, return_type="string"):
    factor = 10 ** decimal_places
    truncated_number = int(number * factor) / factor
    if truncated_number == int(truncated_number): truncated_number = int(truncated_number)
    if return_type != "string": return truncated_number
    return f'{truncated_number:.{decimal_places}f}'.rstrip('0').rstrip('.')

def get_bid_ask(symbol):
    """ 使用 yfinance 获取 bid 和 ask 价格 """
    stock = yf.Ticker(symbol) # ; print(symbol, stock.info)
    
    # 获取当前的买入价和卖出价
    bid = stock.info['bid'] if "bid" in stock.info else 0
    ask = stock.info['ask'] if "ask" in stock.info else 0
    return bid, ask

def get_available_funds():
    """ 获取账户可用资金 """
    account_summary = ib.accountSummary()
    for item in account_summary:
        if item.tag == 'AvailableFunds':
            return float(item.value)
    return 0.0  # 如果未找到，返回0

# 乱序遍历持仓，低买高卖
def manage_positions(positions, symbols, market_status):
    # 获取所有键，然后乱序
    keys = list(symbols.keys())
    random.shuffle(keys)

    # 以乱序的方式遍历字典
    for symbol in keys:
        params = symbols[symbol]
        buy_value = params['buy_value']
        trade_amount = params['trade_amount']
        
        # US-美股、HK-港股、CN-A股票
        market = params.get('market', "US") # 默认值：US-美股
        is_market_open = market_status[market]
        if not is_market_open: continue

        # 计算默认 sell_value，若未定义则使用默认值
        sell_value = params.get('sell_value', buy_value + trade_amount * 2)

        # 使用 yfinance 获取 bid 和 ask 价格（免费）
        # bid_price, ask_price = get_bid_ask(symbol)

        # 使用 IBKR API 获取 bid 和 ask 价格（非专业订阅：NASDAQ $1.50/月，NYSE $1.50/月）      
        stock = Stock(symbol, 'SMART', 'USD')
        ticker = ib.reqMktData(stock) # , regulatorySnapshot=False
        ib.sleep(3); bid_price = ticker.bid; ask_price = ticker.ask

        # 检查 bid 和 ask 价格是否有效
        if not (bid_price > 0 and ask_price > 0):
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"无法获取 {symbol} 的 bid 或 ask 价格。")
            continue

        # 计算动态交易金额：除IBKR API外，所有IBKR平台均支持小数股。
        # https://www.interactivebrokers.com.hk/cn/trading/fractional-trading.php
        if trade_amount <= ask_price + 1:
            trade_amount = int(ask_price + 1)
            sell_value = buy_value + round(trade_amount * 1.96, 0)
            # print(time.strftime("%Y-%m-%d %H:%M:%S"), symbol, "buy_value", buy_value, "trade_amount", trade_amount, "sell_value", sell_value)

        # 获取当前持仓数量
        current_amount = 0
        for position in positions:
            if position.contract.symbol == symbol:
                current_amount = position.position #; print(position)
                break
        # if current_amount <= 0: print(f"无法获取 {symbol} 的持仓数量。"); continue

        bid_value = round(bid_price * current_amount, 2)
        ask_value = round(ask_price * current_amount, 2)
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"{symbol} 当前 bid_price: {bid_price} ask_price: {ask_price} bid_value: {bid_value}, ask_value: {ask_value}")

        # 是否开盘
        is_market_open = get_market_status(market)
        if not is_market_open: continue # 未开盘
        if not ib.isConnected(): break  # 未连接
        
        # 判断是否需要买入
        if ask_value <= buy_value:
            trade_amount_ex = buy_value - ask_value + trade_amount / 2
            quantity = round(max(trade_amount, trade_amount_ex) / ask_price, 0)
            if quantity <= 0: print("trade_amount / ask_price <= 0"); continue
            required_funds = ask_price * quantity 
            # 获取可用资金
            available_funds = get_available_funds()
            if required_funds <= available_funds:
                print(f"市价买入 {quantity} 股的 {symbol}，价格: {ask_price}，金额：{truncate(required_funds, 2)}。")
                order = MarketOrder('BUY', quantity) # order = LimitOrder("BUY", quantity, ask_price)
                trade = ib.placeOrder(Stock(symbol, 'SMART', 'USD'), order)
                ib.waitOnUpdate(); ib.sleep(1)
                # print("trade", trade)
            else:
                print(f"资金不足，无法买入 {symbol}。所需资金: {required_funds}, 可用资金: {available_funds}")

        # 判断是否需要卖出
        elif bid_value >= sell_value:
            trade_amount_ex = bid_value - sell_value + trade_amount
            quantity = round(trade_amount_ex / bid_price, 0)
            if quantity <= 0: print("trade_amount / bid_price <= 0"); continue
            print(f"市价卖出 {quantity} 股的 {symbol}，价格: {bid_price}，金额：{truncate(bid_price * quantity, 2)}。")
            order = MarketOrder('SELL', quantity) # order = LimitOrder("SELL", quantity, bid_price)
            trade = ib.placeOrder(Stock(symbol, 'SMART', 'USD'), order)
            ib.waitOnUpdate(); ib.sleep(1)
            # print("trade", trade)

# 循环获取持仓，低买高卖
try:
    while True:
        try:
            if not ib.isConnected(): ib.connect('127.0.0.1', 4001, clientId=1)

            # 获取账户余额信息
            account_summary = ib.accountSummary()

            # 简单获取美元可用余额和总市值
            available_funds = next((item.value for item in account_summary if item.tag == 'AvailableFunds' and item.currency == 'USD'), 0)
            net_liquidation = next((item.value for item in account_summary if item.tag == 'NetLiquidation' and item.currency == 'USD'), 0)

            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"可用余额: {available_funds} USD", f"总市值: {net_liquidation} USD")

            # 检查 美股、港股、A股 是否开盘
            market_status = { "US": False, "HK": False, "CN": False }
            market_status["US"] = get_market_status('US')
            market_status["HK"] = get_market_status('HK')
            market_status["CN"] = get_market_status('CN')
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"开盘状态: US: {'开盘' if market_status['US'] else '未开盘'} HK: {'开盘' if market_status['HK'] else '未开盘'} CN: {'开盘' if market_status['CN'] else '未开盘'}")
            
            if market_status["US"] or market_status["HK"] or market_status["CN"]:
                # 获取当前持仓
                positions = ib.positions()

                # 调用管理函数
                manage_positions(positions, symbols, market_status)
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
        finally:
            # 休息时间
            time.sleep(300)
        
except KeyboardInterrupt:
    print("手动停止了循环。")

finally:
    # 断开连接
    ib.disconnect()
