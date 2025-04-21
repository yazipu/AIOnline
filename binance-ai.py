# -*- coding: utf-8 -*-
import re, time, binance
from binance.client import Client
import requests
import hashlib
import hmac
    
# API密钥: 主账户
api_key = ""
api_secret = ""
# API密钥：带单账户
copy_key = ""
copy_secret = ""

virtual_balance_enable = False # 是否启用虚拟余额
usdt_keep = 500     # 保持现货 USDT 余额
keep_step = 100     # 每次赎回 USDT 金额
fdusd_keep = 150    # 保持现货 FDUSD 余额
fdusd_step = 50     # 每次赎回 FDUSD 金额
spot_holding = 0 # 现货：0-正常持币，4-立刻清仓
spot_position = 1 # 现货仓位：1-100%仓位，0.9-90%仓位，1.1-110%仓位

# 现货交易对
symbols_spot = {
    'BTCUSDT': { 'buy_value': 1280, 'trade_amount': 25 },
    'ETHUSDT': { 'buy_value': 980, 'trade_amount': 17 },
    'BNBUSDT': { 'buy_value': 200, 'trade_amount': 11,'vb':0 },
    # 'SOLUSDT': { 'buy_value': 390, 'trade_amount': 11 },
    # 'TRXUSDT': { 'buy_value': 190, 'trade_amount': 11 },
    # 'XRPUSDT': { 'buy_value': 190, 'trade_amount': 11 },
}
# 带单交易对
symbols_copy = {
    'BTCUSDT': { 'buy_value': 990, 'trade_amount': 21,'vb':0 },
    'ETHUSDT': { 'buy_value': 490, 'trade_amount': 15,'vb':0 },
    # 'SOLUSDT': { 'buy_value': 390, 'trade_amount': 12 },
    # 'BNBUSDT': { 'buy_value': 290, 'trade_amount': 11 },
    # 'XRPUSDT': { 'buy_value': 190, 'trade_amount': 11 },
}

# 截断小数，不四舍五入
def truncate(number, decimal_places, return_type="string"):
    factor = 10 ** decimal_places
    truncated_number = int(number * factor) / factor
    if truncated_number == int(truncated_number): truncated_number = int(truncated_number)
    if return_type != "string": return truncated_number
    return f'{truncated_number:.{decimal_places}f}'.rstrip('0').rstrip('.')

# 获取理财
# https://binance-docs.github.io/apidocs/spot/cn/#user_data-70
def get_simple_earn_flexible_position(asset="", current = 1, size = 100, copy = False):
    api_key_ex = api_key; api_secret_ex = api_secret
    if copy: api_key_ex = copy_key; api_secret_ex = copy_secret
    # 构建请求参数
    params = {
        'asset': asset,
        'current': current,
        'size': size,
        'timestamp': int(time.time() * 1000)  # 添加时间戳
    }

    # 构建请求头
    headers = {
        'X-MBX-APIKEY': api_key_ex
    }

    # 创建签名
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(api_secret_ex.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    params['signature'] = signature

    # 执行 GET 请求
    url = 'https://api.binance.com/sapi/v1/simple-earn/flexible/position'
    response = requests.get(url, params=params, headers=headers, timeout=(10,30))

    return response.json()

# 申购理财
def subscribe_simple_earn_flexible_product(product_id, amount, copy = False):
    api_key_ex = api_key; api_secret_ex = api_secret
    if copy: api_key_ex = copy_key; api_secret_ex = copy_secret
    # 构建请求参数
    params = {
        'productId': product_id,
        'amount': amount,
        'timestamp': int(time.time() * 1000)  # 添加时间戳
    }

    # 构建请求头
    headers = {
        'X-MBX-APIKEY': api_key_ex
    }

    # 创建签名
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(api_secret_ex.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    params['signature'] = signature

    # 执行 POST 请求
    url = 'https://api.binance.com/sapi/v1/simple-earn/flexible/subscribe'
    response = requests.post(url, params=params, headers=headers, timeout=(10,30))

    json = response.json()
    time.sleep(0.5)
    return json

# 赎回理财
def redeem_simple_earn_flexible_product(product_id, amount, copy = False):
    api_key_ex = api_key; api_secret_ex = api_secret
    if copy: api_key_ex = copy_key; api_secret_ex = copy_secret
    # 构建请求参数
    params = {
        'productId': product_id,
        'amount': amount,
        'timestamp': int(time.time() * 1000)  # 添加时间戳
    }

    # 构建请求头
    headers = {
        'X-MBX-APIKEY': api_key_ex
    }

    # 创建签名
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(api_secret_ex.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    params['signature'] = signature

    # 执行 POST 请求
    url = 'https://api.binance.com/sapi/v1/simple-earn/flexible/redeem'
    response = requests.post(url, params=params, headers=headers, timeout=(10,30))

    json = response.json()
    time.sleep(0.5)
    return json

# 连接到币安API客户端
client_spot = None if api_key == api_secret == "" else Client(api_key, api_secret)      # 现货
client_copy = None if copy_key == copy_secret == "" else Client(copy_key, copy_secret)  # 现货带单
if client_spot == None and client_copy == None: print("API密钥未配置!!!"); exit()
version = binance.__version__
print(time.strftime("%Y-%m-%d %H:%M:%S"), f"python-binance 当前版本 {version}")

# 获取所有现货交易对信息
exchange_info = client_spot.get_exchange_info() if client_spot != None else client_copy.get_exchange_info()

# # 打印所有交易对信息
# for symbol_info in exchange_info['symbols']:
#     symbol = symbol_info['symbol']
#     print(symbol)

# 循环检测和交易
copy = True
while True:
    try:
        i = 0
        if client_spot != None and client_copy != None: copy = not copy # 现货/带单 交替
        elif client_spot != None: copy = False  # 仅现货
        elif client_copy != None: copy = True   # 仅带单
        if copy: client = client_copy; symbols = symbols_copy   # 带单交易对
        else: client = client_spot; symbols = symbols_spot      # 现货交易对

        # 查询现货余额
        account_info = client.get_account()
        balance_list = account_info["balances"]
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"现货数量:", len(balance_list), "是否带单", copy)
        
        # 查询未配置现货余额
        for balance in balance_list:
            coin_balance = round(float(balance['free']), 2)
            if coin_balance == 0 or balance["asset"] in ["USDT", "FDUSD", "LDUSDT", "LDFDUSD", "LDUSDC"]: continue
            exist = False
            for symbol, values in symbols.items():
                coin = symbol[:-5] if "FDUSD" in symbol else symbol[:-4]
                if balance['asset'] == coin or balance["asset"] == "LD" + coin: exist = True; break
            if exist == False: print(balance['asset'], "余额", coin_balance, "未配置！")
        
        # 查询理财余额
        flexible_list = []
        for page in range(1, 1000):
            flexible_info = get_simple_earn_flexible_position("", page, 100, copy)
            flexible_rows = flexible_info.get("rows")
            flexible_list.extend(flexible_rows)
            if len(flexible_rows) < 100: break
        for flexible in flexible_list:
            coin_balance = round(float(flexible['totalAmount']), 2)
            if coin_balance == 0 or flexible["asset"] in ["USDT", "FDUSD"]: continue
            exist = False
            for symbol, values in symbols.items():
                coin = symbol[:-5] if "FDUSD" in symbol else symbol[:-4]
                if flexible['asset'] == coin: exist = True; break
            if exist == False: print(flexible['asset'], "理财", coin_balance, "未配置！")
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"理财数量:", len(flexible_list))

        # https://binance-docs.github.io/apidocs/spot/cn/#5393cd07b4
        ticker_list = client.get_orderbook_tickers()
        ticker_time = int(time.time() * 1000) + 1500
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"行情数量: {len(ticker_list)}  时间戳: {ticker_time}")
        if len(ticker_list) < 100: time.sleep(5); continue

        # 检查BNB现货余额，用于支付交易手续费
        bnb_balance = next((data for data in balance_list if data["asset"] == "BNB"), {"free":0})
        bnb_info = next((data for data in flexible_list if data["asset"] == "BNB"), {"totalAmount":0})
        bnb_flexible = float(bnb_info["totalAmount"]) # if bnb_info.get("rows") else 0.0
        if float(bnb_balance["free"]) < 0.1 and bnb_flexible >= 0.1:
            result = redeem_simple_earn_flexible_product("BNB001", 0.1, copy)
            if not result.get("success"): print(f"赎回 BNB001 失败: {result}")
            
        # 检查USDT现货余额
        usdt_balance = float(next((data["free"] for data in balance_list if data["asset"] == "USDT"), 0))
        usdt_flexible = float(next((data["totalAmount"] for data in flexible_list if data["asset"] == "USDT"), 0))
        if not copy:
            if float(usdt_balance) < usdt_keep and usdt_flexible >= keep_step:
                result = redeem_simple_earn_flexible_product("USDT001", keep_step, copy)
                if not result.get("success"): print(f"赎回 USDT001 失败: {result}")
            elif usdt_balance > usdt_keep * 3:
                lend_usdt = int(usdt_balance - usdt_keep * 2)
                result = subscribe_simple_earn_flexible_product("USDT001", lend_usdt, copy)
                print(f"申购 USDT 金额 {lend_usdt} 结果: {result}")
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"USDT:{round(usdt_balance,2)}  活期:{round(usdt_flexible,2)}")

        # 检查FDUSD现货余额
        fdusd_balance = float(next((data["free"] for data in balance_list if data["asset"] == "FDUSD"), 0))
        fdusd_flexible = float(next((data["totalAmount"] for data in flexible_list if data["asset"] == "FDUSD"), 0))
        if not copy:
            if float(fdusd_balance) < fdusd_keep and fdusd_flexible >= fdusd_step:
                result = redeem_simple_earn_flexible_product("FDUSD001", fdusd_step, copy)
                if not result.get("success"): print(f"赎回 FDUSD001 失败: {result}")
            elif fdusd_balance > fdusd_keep * 3:
                lend_fdusd = int(fdusd_balance - fdusd_keep * 2)
                result = subscribe_simple_earn_flexible_product("FDUSD001", lend_fdusd, copy)
                print(f"申购 FDUSD 金额 {lend_fdusd} 结果: {result}")
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"FDUSD:{round(fdusd_balance,2)}  活期:{round(fdusd_flexible,2)}")
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "Exception:", str(e))
        time.sleep(30)
        continue
    
    sleep_time = 90; sum_buy_value = 0; sum_spot_value = 0; sold_coin = err_coin = zero_coin = ""; order_time = time.time()
    for symbol, values in symbols.items():
        try:
            i = i + 1

            coin = symbol[:-5] if "FDUSD" in symbol else symbol[:-4]
            currency = symbol.replace(coin, '', 1)
            # 查找数量小数位数
            filters = next(filter(lambda s: s['symbol'] == symbol, exchange_info['symbols']))['filters']
            precision = int(next(filter(lambda f: f['filterType'] == 'LOT_SIZE', filters))['stepSize'].find('1')) - 1
            if precision < 0: precision = 0

            # 获取账户余额和当前价格
            flexible_balance = 0
            asset_balance = next((data for data in balance_list if data["asset"] == coin), {"free":0})
            position_info = next((data for data in flexible_list if data["asset"] == coin), {"totalAmount":0})
            flexible_balance = float(position_info["totalAmount"]) # if position_info.get("rows") else 0.0
            symbol_balance = float(asset_balance['free']) + flexible_balance
            if ticker_time < int(time.time() * 1000):
                ticker_list = client.get_orderbook_tickers()
                # print(time.strftime("%Y-%m-%d %H:%M:%S"), f"行情数量: {len(ticker_list)}  时间戳: {ticker_time}")
                if len(ticker_list) < 100: continue
                ticker_time = int(time.time() * 1000) + 1500
            ticker_info = next((data for data in ticker_list if data["symbol"] == symbol), {"bidPrice":0,"askPrice":0})
            buy_price = float(ticker_info['bidPrice'])
            sell_price = float(ticker_info['askPrice'])

            # 虚拟余额
            if int(symbol_balance * buy_price) <= 18: zero_coin += coin + " "
            if buy_price <= 0 or sell_price <= 0: print(f"{i}. {coin} 获取价格失败!!!"); err_coin += coin + " "; continue
            if virtual_balance_enable != True: values['vb'] = 0
            if 'vb' in values: values["virtual_balance"] = values['vb'] / buy_price
            elif not "virtual_balance" in values:
                virtual_balance = max(0, (values["buy_value"] + values["trade_amount"] / 1.2) / buy_price - symbol_balance)
                if virtual_balance * buy_price < values['trade_amount']: virtual_balance = 0
                keep_value = values["kv"] + values["trade_amount"] / 1.8 if "kv" in values else values["trade_amount"] * 2.56
                if symbol_balance * buy_price < keep_value: virtual_balance -= keep_value / buy_price - symbol_balance
                values["virtual_balance"] = max(virtual_balance, 0)
            virtual_balance = values["virtual_balance"] if values["virtual_balance"] * buy_price > values["trade_amount"] else 0
            virtual_buy_value = virtual_balance * buy_price
            # if virtual_balance > 0: print(coin, "virtual_balance", virtual_balance, 'symbol_balance', symbol_balance)
            symbol_balance += virtual_balance

            # 计算账户余额的价值
            buy_value = round(symbol_balance * buy_price, 2)
            sell_value = round(symbol_balance * sell_price, 2)
            sum_buy_value += buy_value; sum_spot_value += buy_value - virtual_buy_value
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"{i}. {coin}  价格:{round(sell_price,10)}  余额 buy:{int(buy_value-virtual_buy_value)}{'+'+str(int(virtual_buy_value)) if virtual_balance>0 else''} sell:{sell_value}"),  # 数量小数位数：{precision}
            
            # 0-正常持币，4-立刻清仓
            if not "st" in values: values["st"] = spot_holding
            if values["st"] == 4: # 立刻清仓
                if flexible_balance > 0:
                    result = redeem_simple_earn_flexible_product(coin+"001", flexible_balance)
                    if not result.get("success"): print(f"赎回 {coin} {flexible_balance} 失败: {result}")
                elif buy_value - virtual_buy_value > 1:
                    quantity = truncate(symbol_balance - virtual_balance, precision)
                    order = client.order_market_sell(symbol=symbol, quantity=quantity); sold_coin += coin + " "
                continue

            # 计算：sell_value
            if not "sell_value" in values:
                if 'sell_valuex' in values: values["sell_value"] = values["sell_valuex"]
                elif values["trade_amount"] < 10: values["sell_value"] = values["buy_value"] + 12
                else: values["sell_value"] = round(values["buy_value"] + values["trade_amount"] * 1.96, 0)
            
            # BNB有launchpad
            if symbol == "BNBUSDT" and sell_value > 1:
                if sell_value > values['sell_value'] * 1.2: continue
                if sell_value < values['sell_value'] * 0.9 and values['buy_value'] > 500: continue

            # 如果价值低于买入价值，则买入指定数量的币种
            if sell_price > 0 and sell_value <= values['buy_value'] and values['buy_value'] > 0:
                quantity = str(round(values['trade_amount'] / sell_price, precision)); order = None
                print(time.strftime("%Y-%m-%d %H:%M:%S"), f"买入 {quantity} {coin}，市价为 {sell_price} {currency}")
                currency_balance = fdusd_balance if currency == "FDUSD" else usdt_balance
                if currency_balance >= values['trade_amount']:
                    order = client.order_market_buy(symbol=symbol, quantity=quantity)
                else:
                    time.sleep(0.07)
                    currency_flexible_balance = fdusd_flexible if currency == "FDUSD" else usdt_flexible
                    if currency_flexible_balance >= min(1000, values['trade_amount'] * 10):
                        result = redeem_simple_earn_flexible_product(currency+"001", min(1000, values['trade_amount'] * 10), copy)
                        if result == None or not result.get("success"): print(f"赎回 {currency} 失败: {result}")
                        else: order = client.order_market_buy(symbol=symbol, quantity=quantity)
                        if currency == "FDUSD": fdusd_flexible -= values['trade_amount'] * 10; fdusd_balance += values['trade_amount'] * 10
                        else: usdt_flexible -= values['trade_amount'] * 10; usdt_balance += values['trade_amount'] * 10
                if order != None and 'orderId' in order:
                    if virtual_balance > 0: virtual_balance -= values['trade_amount'] / buy_price / 10
                    if currency == "FDUSD": fdusd_balance -= values['trade_amount']
                    else: usdt_balance -= values['trade_amount']
                # print(f"买入 {quantity} {coin}，成交价为 {round(order['fills'][0]['price'], 8)} {currency}")

            # 如果价值高于卖出价值，则卖出指定数量的币种
            elif buy_value >= values['sell_value']:
                trade_amount = buy_value - values['sell_value'] + values['trade_amount']
                quantity = str(round(trade_amount / buy_price, precision))
                print(time.strftime("%Y-%m-%d %H:%M:%S"), f"卖出 {quantity} {coin}，市价为 {buy_price} {currency}")
                
                # 判断余额是否够卖
                if symbol_balance * buy_price < trade_amount or trade_amount < 5.20: continue
                print(f'{symbol} bv: {values["buy_value"]}, sv: {values["sell_value"]}, ta: {trade_amount}')

                # 现货不够卖，则全部卖出
                if symbol_balance - virtual_balance < float(quantity):
                    quantity = truncate(symbol_balance - virtual_balance, precision)
                    if virtual_balance > 0: virtual_balance -= values['trade_amount'] / buy_price
                elif virtual_balance * buy_price + values["trade_amount"] > values['sell_value']:
                    if virtual_balance > 0: virtual_balance -= values['trade_amount'] / buy_price
                elif virtual_balance > 0: virtual_balance -= values["trade_amount"] / buy_price / 2

                # 理财->现货：要卖出的币
                if flexible_balance >= float(quantity) and float(asset_balance['free']) < float(quantity):
                    redeem_qty = values["redeem_qty"] if "redeem_qty" in values else quantity
                    result = redeem_simple_earn_flexible_product(coin+"001", redeem_qty, copy) # { 'redeemId': 200632906, 'success': True}
                    if not result.get("success"): print(f"赎回 {coin} {redeem_qty} 失败: {result}")
                # 执行卖出
                order = client.order_market_sell(symbol=symbol, quantity=quantity); sold_coin += coin + " "
                # print(f"卖出 {quantity} {coin}，成交价为 {round(order['fills'][0]['price'], 8)} {currency}")
            if values["virtual_balance"] > virtual_balance:
                print("virtual_balance>", values["virtual_balance"], ">", virtual_balance)
                values["virtual_balance"] = virtual_balance if virtual_balance > 0 else 0
            elif values["virtual_balance"] < virtual_balance:
                print("virtual_balance<", values["virtual_balance"], "<", virtual_balance)
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S"), symbol, "Exception:", str(e))
        
        time.sleep(0.03)

    print(time.strftime("%Y-%m-%d %H:%M:%S"), f"sum_buy_value", round(sum_buy_value), "sum_spot_value", round(sum_spot_value), "usdt", round(usdt_balance + usdt_flexible), "fdusd", round(fdusd_balance + fdusd_flexible))
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "sold_coin", sold_coin, "err_coin", err_coin, "zero_coin", zero_coin, "copy", copy)
    
    # 休息时间
    time.sleep(sleep_time)
