# -*- coding: utf-8 -*-
# https://www.bitget.com/zh-CN/api-doc/spot/intro
import time, pybitget
from pybitget import Client
import requests, json, hashlib, hmac, time, base64

# 设置API密钥和密钥
api_key = ''
api_secret = ''
api_passphrase = ''

auto_redeem_usdt = False # False：手工控管资金，手工从理财赎回 USDT，True：自动从理财赎回 USDT
usdt_keep_step = 250 # 当BTC或ETH需要补仓时，从理财中赎回USDT的金额

virtual_balance_enable = False # 是否启用虚拟余额
usdt_keep = 1000    # 保持现货 USDT 余额
keep_step = 100     # 每次赎回 USDT 金额
bgb_keep = 10       # 保持现货 BGB  余额

# 设置要检测的币种和相应的价值判断
symbols = {
    # 平台币
    'BGBUSDT': { 'buy_value': 190, 'trade_amount': 11, 'top': 84,'earn':50,'kv':30,'spot_only':1,'st':0 },

    # 高单价暂时不带：获利了结，落袋为安
    'GMTUSDT': { 'lead_price': 0.5, 'buy_value': 570, 'trade_amount': 30, 'profit_rate': 1.031, 'top': 118,'st':0 }, # 60 GMT

    # TOP 100
    'BTCUSDT': { 'lead_price': 550000, 'buy_value': 10150, 'trade_amount': 110, 'profit_rate': 1.011, 'top': 1, 'minStepVal': 0.001,'vb':0,'st':0 }, # 0.0002 BTC
    'ETHUSDT': { 'lead_price': 11000, 'buy_value': 5150, 'trade_amount': 55, 'profit_rate': 1.011, 'top': 2,'vb':0,'st':0 }, # 0.005 ETH

    # 候补交易对
    'FILUSDT': { 'lead_price': 15, 'buy_value': 570, 'trade_amount': 30, 'top': 33 }, # 2 FIL

    # 无带单交易对
    'CRVUSDT': { 'buy_value': 190, 'trade_amount': 11, 'top': 113 },

    # 带单交易对
    'OPUSDT': { 'lead_price': 5, 'buy_value': 570, 'trade_amount': 30, 'top': 28 }, # 6 OP
    'PYTHUSDT': { 'lead_price': 1, 'buy_value': 670, 'trade_amount': 35, 'profit_rate': 1.031, 'top': 113 }, # 35 PYTH
    'LDOUSDT': { 'lead_price': 4.4, 'buy_value': 570, 'trade_amount': 30, 'top': 32 }, # 7 LDO
    'JSTUSDT': { 'lead_price': 0.7, 'buy_value': 950, 'trade_amount': 50, 'profit_rate': 1.025, 'top': 172 }, # 700 JST
    'GMXUSDT': { 'lead_price': 130, 'buy_value': 570, 'trade_amount': 30, 'top': 119 }, # 0.4 GMX
    'CAKEUSDT': { 'lead_price': 6, 'buy_value': 570, 'trade_amount': 30, 'top': 79 }, # 5 CAKE
    'STXUSDT': { 'lead_price': 4.4, 'buy_value': 570, 'trade_amount': 30, 'top': 39 }, # 7 STX

    # 减少带单，待观察
    'POLUSDT': { 'lead_price': 1, 'buy_value': 290, 'trade_amount': 15, 'top': 14,'st':0 }, # 15 POL

    # 获利了结，停止带单
    # 'KEYUSDT': { 'lead_price': 0.088, 'buy_value': 190, 'trade_amount': 11, 'profit_rate': 1.051, 'top': 625,'st':1 }, # 2000 KEY

    # 停止买入
    'WLDUSDT': { 'lead_price': 1.1, 'buy_value': 0, 'sell_valuex': 210, 'trade_amount': 11, 'profit_rate': 1.041, 'top': 144 }, # 10 WLD

    # 暂停交易
    'RONUSDT': { 'lead_price': 0.55, 'buy_value': 0, 'sell_valuex': 210, 'trade_amount': 11, 'top': 101,'st':0 }, # 20 RON
 
    # 清仓
    # 'FLOKIUSDT': { 'lead_price': 0.0000111, 'buy_value': 0, 'sell_valuex': 210, 'trade_amount': 11, 'profit_rate': 1.033, 'top': 150,'st':4 }, # 400000 FLOKI
    # 'SLPUSDT': { 'lead_price': 0.00111, 'buy_value': 0, 'sell_valuex': 210, 'trade_amount': 11, 'profit_rate': 1.031, 'top': 63,'st':4 },
    # 'XLMUSDT': { 'lead_price': 0.99, 'buy_value': 570, 'trade_amount': 30, 'top': 26,'st':4 }, # 165 XLM

    # 获利了结，停止带单
    'APTUSDT': { 'lead_price': 10, 'buy_value': 380, 'trade_amount': 20, 'top': 25,'st':0 }, # 2 APT
    'DOTUSDT': { 'lead_price': 3.66, 'buy_value': 190, 'trade_amount': 11, 'top': 11,'st':0 }, # 3 DOT
    'DOGEUSDT': { 'lead_price': 0.2, 'buy_value': 480, 'trade_amount': 24, 'top': 10,'st':0 }, # 120 DOGE
    'LINKUSDT': { 'lead_price': 1, 'buy_value': 190, 'trade_amount': 11, 'top': 13,'st':0 }, # 3 LINK (LINK币带单额度不足，不要带单)
    'LTCUSDT': { 'lead_price': 70, 'buy_value': 380, 'trade_amount': 21, 'profit_rate': 1.0151, 'top': 19,'st':0 }, # 0.3 LTC
    'SHIBUSDT': { 'lead_price': 0.00000111, 'buy_value': 190, 'trade_amount': 11, 'top': 16,'st':0 }, # 466000 SHIB
    'TRXUSDT': { 'lead_price': 0.04, 'buy_value': 200, 'trade_amount': 12, 'top': 11,'st':0 }, # 300 TRX
    'UNIUSDT': { 'lead_price': 2.75, 'buy_value': 190, 'trade_amount': 11, 'profit_rate': 1.021, 'top': 22,'st':0 }, # 4 UNI
    'XRPUSDT': { 'lead_price': 0.5, 'buy_value': 280, 'trade_amount': 15, 'profit_rate': 1.013, 'top': 4,'st':0 }, # 30 XRP
    
}

# 构造请求头 https://bitgetlimited.github.io/apidoc/zh/copyTrade/#8ba46c43fe
def get_bitget_headers(api_key, api_secret, api_passphrase, method, path, query_string="", body=""):
    timestamp = int(time.time())*1000
    # 构建待签名字符串
    if query_string:
        message = f'{timestamp}{method.upper()}{path}?{query_string}{body}'
    else:
        message = f'{timestamp}{method.upper()}{path}{body}'
    # print("message", message)

    # 使用私钥进行 HMAC SHA256 加密
    signature = hmac.new(api_secret.encode(), message.encode(), hashlib.sha256).digest()

    # 对签名进行 Base64 编码
    signature_b64 = base64.b64encode(signature).decode()

    headers = {
        'ACCESS-KEY': api_key,
        'ACCESS-SIGN': signature_b64,
        'ACCESS-PASSPHRASE': api_passphrase,
        'ACCESS-TIMESTAMP': str(timestamp),
        'Content-Type': 'application/json',
    }

    # print("get_bitget_headers", headers)
    return headers

# 获取当前带单V2 https://www.bitget.com/zh-CN/api-doc/copytrading/spot-copytrade/trader/Order-Current-Track
def get_order_current_track(api_key, api_secret, api_passphrase, idLessThan="", limit=50, symbol=""):
    try:
        base_url = 'https://api.bitget.com'
        path = '/api/v2/copy/spot-trader/order-current-track'
        url = base_url + path
        params = {
            'idLessThan': idLessThan,
            'limit': limit,
            'symbol': symbol,
        }
        query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())]) if params else ""
        # print(url, query_string)
        headers = get_bitget_headers(api_key, api_secret, api_passphrase, 'GET', path, query_string)
        response = requests.get(url, headers=headers, params=params, timeout=(20,60))

        if response.status_code == 200:
            return response.json()
        else:
            print(f"获取带单列表失败: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
    return None

# 关闭带单V2
def close_tracking_order_v2(api_key, api_secret, api_passphrase, symbol, trackingNoList):
    try:
        base_url = 'https://api.bitget.com'
        path = "/api/v2/copy/spot-trader/order-close-tracking"
        url = base_url + path
        close_order_params = {
            'symbol': symbol,
            'trackingNoList': trackingNoList,
        }
        data=json.dumps(close_order_params, separators=(',', ':'))
        headers = get_bitget_headers(api_key, api_secret, api_passphrase, 'POST', path, "", data)
        response = requests.post(url, headers=headers, data=data, timeout=(20,60))

        # 处理卖出响应
        if response.status_code == 200:
            return True, response.json()
        else:
            print(f"卖出V2失败: {response.status_code}, {response.text}")
            return False, None
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
    return False, None

# 现货下单： https://www.bitget.com/zh-CN/api-doc/spot/trade/Place-Order
def spot_place_order(api_key, api_secret, api_passphrase, symbol, side, orderType, force, size, price = 0):
    try:
        base_url = 'https://api.bitget.com'
        path = '/api/v2/spot/trade/place-order'
        url = base_url + path        
        params = {
            'symbol': symbol,
            'side': side,
            'orderType': orderType,
            'force': force,
            'size': size,
        }
        if price > 0: params["price"] = price
        data=json.dumps(params, separators=(',', ':'))
        headers = get_bitget_headers(api_key, api_secret, api_passphrase, 'POST', path, "", data)
        response = requests.post(url, headers=headers, data=data, timeout=(20,60))

        # 处理卖出响应
        if response.status_code == 200:
            return response.json()
        else:
            print(f"现货下单失败: {response.status_code}, {response.text}")
            return response.json()
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
    return None

# 查找并关闭盈利最多的带单
def close_most_profitable_order(orders, symbol, price, rate = 1.0125):
    global api_key, api_secret, api_passphrase
    # 初始化最大盈利和对应带单
    min_buy_price = 0
    max_buy_price = 0
    min_buy_price_order = None
    if orders and len(orders) > 0:

        # 在这里遍历 orders，找到盈利最多的带单
        for order in orders:
            if order['symbol'] == symbol:
                if float(order['buyPrice']) > max_buy_price: max_buy_price = float(order['buyPrice'])
                if float(order['buyPrice']) < min_buy_price or min_buy_price == 0:
                    min_buy_price = float(order['buyPrice'])
                    min_buy_price_order = order

        # 判断是否找到盈利最多的带单
        if min_buy_price_order and price > min_buy_price * rate:
            # 卖出带单
            success, result = close_tracking_order_v2(api_key, api_secret, api_passphrase, symbol, [min_buy_price_order['trackingNo']])
            if success:
                orders.remove(min_buy_price_order)
                print(f"成功卖出: {symbol} {json.dumps(result, separators=(',', ':'))}"); time.sleep(0.5)
                return orders, min_buy_price, max_buy_price
            else:
                # print("关闭带单失败，尝试卖出现货")
                return False, min_buy_price, max_buy_price
        else:
            # print(f"未找到符合条件的带单(symbol: {symbol})")
            return False, min_buy_price, max_buy_price
    else:
        # print("获取带单列表失败或列表为空")
        return False, min_buy_price, max_buy_price

# 获取行情信息： https://www.bitget.com/zh-CN/api-doc/spot/market/Get-Tickers
def get_spot_market_tickers(api_key, api_secret, api_passphrase, symbol = ""):
    try:
        base_url = 'https://api.bitget.com'
        path = '/api/v2/spot/market/tickers'
        url = base_url + path 
        params = { }
        if symbol: params["symbol"] = symbol
        query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())]) if params else ""
        headers = get_bitget_headers(api_key, api_secret, api_passphrase, 'GET', path, query_string)
        response = requests.get(url, headers=headers, params=params, timeout=(20,60))

        if response.status_code == 200:
            return response.json()
        else:
            print(f"获取账户现货资产失败: {response.status_code}, {response.text}")
            return response.json()
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
    return None

# 获取账户现货资产： https://www.bitget.com/zh-CN/api-doc/spot/account/Get-Account-Assets
def get_spot_account_assets(api_key, api_secret, api_passphrase, coin = "", assetType = "hold_only"):
    try:
        base_url = 'https://api.bitget.com'
        path = '/api/v2/spot/account/assets'
        url = base_url + path
        params = {
            'assetType': assetType,
        }
        if coin != "": params["coin"] = coin
        query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())]) if params else ""
        headers = get_bitget_headers(api_key, api_secret, api_passphrase, 'GET', path, query_string)
        response = requests.get(url, headers=headers, params=params, timeout=(20,60))

        if response.status_code == 200:
            return response.json()
        else:
            print(f"获取账户现货资产失败: {response.status_code}, {response.text}")
            return response.json()
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
    return None

# 查询理财宝产品列表： https://www.bitget.com/zh-CN/api-doc/earn/savings/Savings-Products
def get_savings_product(api_key, api_secret, api_passphrase, coin, filter="available_and_held"):
    try:
        base_url = 'https://api.bitget.com'
        path = '/api/v2/earn/savings/product'
        url = base_url + path 
        params = {
            'coin': coin,
            'filter': filter,
        }
        query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())]) if params else ""
        headers = get_bitget_headers(api_key, api_secret, api_passphrase, 'GET', path, query_string)
        response = requests.get(url, headers=headers, params=params, timeout=(20,60))

        if response.status_code == 200:
            return response.json()
        else:
            print(f"获取理财宝产品列表失败: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
    return None

# 查询活期理财宝资产信息： https://www.bitget.com/zh-CN/api-doc/earn/savings/Savings-Assets
# curl "https://api.bitget.com/api/v2/earn/savings/assets?periodType=flexible&pageSize=20&idLessThan="
def get_savings_assets_list(api_key, api_secret, api_passphrase, periodType="flexible" , idLessThan="", limit=20):
    try:
        base_url = 'https://api.bitget.com'
        path = '/api/v2/earn/savings/assets'
        url = base_url + path
        params = {
            'idLessThan': idLessThan,
            'limit': limit,
            'periodType': periodType,
        }
        query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())]) if params else ""
        headers = get_bitget_headers(api_key, api_secret, api_passphrase, 'GET', path, query_string)
        response = requests.get(url, headers=headers, params=params, timeout=(20,60))

        if response.status_code == 200:
            return response.json()
        else:
            print(f"获取活期理财宝资产信息失败: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
    return None

# 活期理财宝申购： https://www.bitget.com/zh-CN/api-doc/earn/savings/Savings-Subscribe
def savings_subscribe(api_key, api_secret, api_passphrase, periodType, productId, amount):
    try:
        base_url = 'https://api.bitget.com'
        path = '/api/v2/earn/savings/subscribe'
        url = base_url + path
        params = {
            'amount': amount,
            'periodType': periodType,
            'productId': productId,
        }
        data=json.dumps(params, separators=(',', ':'))
        headers = get_bitget_headers(api_key, api_secret, api_passphrase, 'POST', path, "" , data)
        response = requests.post(url, headers=headers, data=data, timeout=(20,60))

        if response.status_code == 200:
            return response.json()
        else:
            print(f"申购失败: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
    return None

# 活期理财宝赎回： https://www.bitget.com/zh-CN/api-doc/earn/savings/Savings-Redeem
def savings_redeem(api_key, api_secret, api_passphrase, periodType, productId, amount):
    try:
        base_url = 'https://api.bitget.com'
        path = '/api/v2/earn/savings/redeem'     
        url = base_url + path
        params = {
            'amount': amount,
            'periodType': periodType,
            'productId': productId,
        }
        data=json.dumps(params, separators=(',', ':'))
        headers = get_bitget_headers(api_key, api_secret, api_passphrase, 'POST', path, "" , data)
        response = requests.post(url, headers=headers, data=data, timeout=(20,60))

        if response.status_code == 200:
            return response.json()
        else:
            print(f"赎回失败: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
    return None

# 交易员查询带单设置： https://www.bitget.com/zh-CN/api-doc/copytrading/spot-copytrade/trader/Config-Query-Settings
def get_spot_trader_setting(api_key, api_secret, api_passphrase):
    try:
        base_url = 'https://api.bitget.com'
        path = '/api/v2/copy/spot-trader/config-query-settings'
        url = base_url + path
        params = { }
        query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())]) if params else ""
        headers = get_bitget_headers(api_key, api_secret, api_passphrase, 'GET', path, query_string)
        response = requests.get(url, headers=headers, params=params, timeout=(20,60))

        if response.status_code == 200:
            return response.json()
        else:
            print(f"查询交易员现货带单设置失败: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
    return None

# 带单币对设置:  https://www.bitget.com/zh-CN/api-doc/copytrading/spot-copytrade/trader/Config-Setting-Symbols
def spot_trader_symbols(api_key, api_secret, api_passphrase, symbolList, settingType):
    try:
        base_url = 'https://api.bitget.com'
        path = '/api/v2/copy/spot-trader/config-setting-symbols'     
        url = base_url + path
        params = {
            'settingType': settingType,
            'symbolList': symbolList,
        }
        data=json.dumps(params, separators=(',', ':'))
        headers = get_bitget_headers(api_key, api_secret, api_passphrase, 'POST', path, "" , data)
        response = requests.post(url, headers=headers, data=data, timeout=(20,60))

        if response.status_code == 200:
            return response.json()
        else:
            print(f"失设置败: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
    return None

# 是否开启带单
def spot_trace_enable(spot_trace_list, symbol):
    trace_enable = ''
    for trace_symbol in spot_trace_list:
        if trace_symbol["symbol"] == symbol:
            trace_enable = 'add' if trace_symbol['enable'] == 'YES' else 'delete'
            break
    return trace_enable

# 截断小数，不四舍五入
def truncate(number, decimal_places, return_type="string"):
    factor = 10 ** decimal_places
    truncated_number = int(number * factor) / factor
    if truncated_number == int(truncated_number): truncated_number = int(truncated_number)
    if return_type != "string": return truncated_number
    return f'{truncated_number:.{decimal_places}f}'.rstrip('0').rstrip('.')

# 连接到Bitget API客户端
client = Client(api_key, api_secret, api_passphrase)
version = pybitget.__version__
print(time.strftime("%Y-%m-%d %H:%M:%S"), f"python-bitget 当前版本 {version}")

# 获取现货交易对精度
result = client.spot_get_symbols()
if result != None and result["code"] == "00000":
    spot_symbols = result["data"]
    for symbol, values in symbols.items():
        values["priceScale"] = values["num_dp"] if "num_dp" in values else 0
        values["quantityScale"] = values["num_dp"] if "num_dp" in values else 0
        if symbol in ["HIPPUSDT":] continue
        for spot_symbol in spot_symbols:
            if symbol == spot_symbol["symbolName"]:
                values["priceScale"] = int(spot_symbol["priceScale"])
                if symbol in ["ZZZUSDT"]: continue
                values["quantityScale"] = int(spot_symbol["quantityScale"])
# print("symbols", symbols)

# 循环检测持仓并交易
savings_product = {}
while True:
    try:
        i = 0
        quantity = 0

        # 查询带单设置
        spot_trader_enable = False
        spot_trace_list = []
        response = get_spot_trader_setting(api_key, api_secret, api_passphrase)
        if response != None and response['code'] == '00000':
            if response['data']['enable'] == 'YES': spot_trader_enable = True
            spot_trace_list = response['data']['traceSymbolList']
            print(time.strftime("%Y-%m-%d %H:%M:%S"), '带单设置', response['data']['enable'], spot_trader_enable)
        
        # 查询活期理财宝资产信息
        retry = 0
        min_id = ""
        savings_list = []
        for page in range(1, 1000):
            result = get_savings_assets_list(api_key, api_secret, api_passphrase, "flexible", min_id, 100)
            if result != None and result["code"] == "00000":
                data = result["data"]
                min_id = data["endId"]
                result_list = data["resultList"]
                savings_list.extend(result_list)
                if len(result_list) < 100: break
                else: time.sleep(0.1)
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S"), f"获取【活期理财宝】资产失败: {result}")
                retry = retry + 1
                if retry > 60: exit()
                else: time.sleep(10)
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "当前【活期理财宝】资产数量", len(savings_list))

        # 获取账户余额
        balances = {}
        response = get_spot_account_assets(api_key, api_secret, api_passphrase)
        if response and response['code'] == '00000':
            balances = response['data']
        else:
            print('获取账户余额失败:', response)
            time.sleep(30); continue
        
        # 检查USDT现货余额
        usdt_product_id = 964334561256718336
        usdt_balance = 0
        usdt_flexible = 0
        # USDT 现货余额
        for balance in balances:
            if balance['coin'] == "USDT":
                usdt_balance = round(float(balance['available']), 6)
                # print('usdt_balance', usdt_balance)
            else:
                exist = False
                for symbol, values in symbols.items():
                    if balance['coin'] == symbol[:-4]:
                        exist = True
                        break
                if exist == False: print(balance['coin'], "余额", round(float(balance['available']), 2), "未配置！")
        # USDT 活期理财余额
        for saving in savings_list:
            if saving['productCoin'] == "USDT":
                usdt_product_id = saving['productId']
                usdt_flexible = round(float(saving['holdAmount']), 6)
                # print('usdt_flexible', usdt_flexible)
                break
        print(f"USDT:{usdt_balance} 活期:{usdt_flexible}")
        if usdt_balance < usdt_keep and usdt_flexible >= keep_step:
            result = savings_redeem(api_key, api_secret, api_passphrase, "flexible", usdt_product_id, keep_step)
            if result and result['code'] == '00000': print(f"赎回 {keep_step} USDT 成功: {result['msg']}")
            else: print(f"赎回 {keep_step} USDT 失败: {result}")
            # time.sleep(5)
        elif usdt_balance > usdt_keep * 3:
            lend_usdt = int(usdt_balance - usdt_keep * 2)
            result = savings_subscribe(api_key, api_secret, api_passphrase, "flexible", usdt_product_id, lend_usdt)
            print(f"申购 USDT 金额 {lend_usdt} 结果: {result}")
        
        # 检查BGB现货余额，用于支付交易手续费
        bgb_product_id = ""
        bgb_balance = 0
        bgb_flexible = 0
        # bgb_copytrade = 0
        # # BGB 带单余额
        # for order in order_list:
        #     if order["symbol"] == "BGBUSDT":
        #         bgb_copytrade += round(float(order["buyFillSize"]), 2) # V2
        # BGB 现货余额
        for balance in balances:
            if balance['coin'] == "BGB":
                bgb_balance = round(float(balance['available']), 2)
                break
        # BGB 活期理财余额
        for saving in savings_list:
            if saving['productCoin'] == "BGB":
                bgb_product_id = saving['productId']
                bgb_flexible = round(float(saving['holdAmount']), 2)
                break
        if bgb_balance < bgb_keep and bgb_flexible >= bgb_keep: # - bgb_copytrade
            result = savings_redeem(api_key, api_secret, api_passphrase, "flexible", bgb_product_id, bgb_keep)
            if result and result['code'] == '00000': print(f"赎回 {bgb_keep} BGB 成功: {result['msg']}")
            else: print(f"赎回 {bgb_keep} BGB 失败: {result}")
        print(f"BGB:{bgb_balance} 活期:{bgb_flexible}") # 带单:{bgb_copytrade}")
        
        # 查询带单列表V2
        retry = 0
        min_id = ""
        order_list = []
        for page in range(1, 1000):
            result = get_order_current_track(api_key, api_secret, api_passphrase, min_id, 50)
            if result != None and result["code"] == "00000":
                data = result["data"]
                min_id = data["endId"]
                result_list = data["trackingList"]
                order_list.extend(result_list)
                # print(page, min_id) # , order_list)
                if len(result_list) < 1: break
                else: time.sleep(0.1)
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S"), f"获取【带单】V2失败: {result}")
                retry = retry + 1
                if retry > 120: exit()
                else: time.sleep(60)
        # print(time.strftime("%Y-%m-%d %H:%M:%S"), "当前带单数量V2", len(order_list))

        # 获取全部行情信息
        ticker_list = []
        ticker_time = int(time.time() * 1000) + 1500
        response = get_spot_market_tickers(api_key, api_secret, api_passphrase)
        if response and response['code'] == '00000': ticker_list = response['data']
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"行情数量: {len(ticker_list)}  时间戳: {ticker_time}")
        if len(ticker_list) < 100: continue
        
        # 计算带单数量、总额及盈利
        order_amount = 0; order_profit = 0; order_symbol = set()
        for order in order_list:
            order_amount += float(order["buyFillSize"]) * float(order['buyPrice'])
            buy_price = next((float(data['bidPr']) for data in ticker_list if data["symbol"] == order["symbol"]), 0)
            if buy_price > 0: order_profit += float(order["buyFillSize"]) * (buy_price - float(order['buyPrice']))
            if not order["symbol"] in order_symbol: order_symbol.add(order["symbol"])
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"当前带单数量V2：{len(order_list)} 币种：{len(order_symbol)} 总额：{round(order_amount,2)} 盈利：{round(order_profit,2)}")
        time.sleep(3)
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "Exception:", str(e))
        time.sleep(30)
        continue

    sleep_time = 50; sum_buy_value = 0; sum_spot_value = 0; sold_coin = err_coin = over_coin = zero_coin = ""; order_time = time.time()
    for symbol, values in symbols.items():
        try:
            i = i + 1
            product_id = ""; coin = symbol[:-4]
            asset_balance = 0; order_balance = 0; saving_balance = 0
            for balance in balances:
                if balance['coin'] == coin:
                    asset_balance = float(balance['available'])
                    if asset_balance == int(asset_balance): asset_balance = int(asset_balance)
                    break
            for saving in savings_list:
                if saving['productCoin'] == coin:
                    product_id = saving["productId"]
                    saving_balance += float(saving['holdAmount'])
                    if saving_balance == int(saving_balance): saving_balance = int(saving_balance)
                    # break
            order_count = 0
            for order in order_list:
                if order['symbol'] == symbol:
                    order_count += 1
                    order_balance += float(order['buyFillSize'])
            symbol_balance = asset_balance + saving_balance
            if "lead_only" in values: symbol_balance = order_balance
            elif "spot_only" in values: symbol_balance = asset_balance - order_balance
            # print("asset_balance", asset_balance, "saving_balance", saving_balance)

            # 获取当前币种价格
            buy_price = 0; sell_price = 0
            if ticker_time < int(time.time() * 1000):
                response = get_spot_market_tickers(api_key, api_secret, api_passphrase)
                if response and response['code'] == '00000': ticker_list = response['data']
                # print(time.strftime("%Y-%m-%d %H:%M:%S"), f"行情数量: {len(ticker_list)}  时间戳: {ticker_time}")
                if len(ticker_list) < 100: continue
                ticker_time = int(time.time() * 1000) + 1500
            for ticker in ticker_list:
                if symbol == ticker["symbol"]:
                    buy_price = float(ticker['bidPr'])
                    sell_price = float(ticker['askPr'])
                    break
            if buy_price <= 0 or sell_price <= 0: print(f"{i}. {coin} 获取价格失败!!!"); err_coin += coin + " "; continue

            # 带单计算：trade_amount
            if int(symbol_balance * buy_price) <= 5: zero_coin += coin + " "
            if not "trade_amount_bak" in values: values["trade_amount_bak"] = values["trade_amount"]
            lead_price = values["lead_price"] if "lead_price" in values else 0
            if lead_price > 0 and values["buy_value"] >= 100 and not 'sell_valuex' in values: # 是否开启带单
                if buy_price > lead_price * 1.02: # 如果当前价大于带单价*1.02：trade_amount = max(当前价*0.02, 10)
                    values["trade_amount"] = max(int(values["buy_value"] * 0.02), 10)
                    values["sell_value"] = 0
                elif sell_price < lead_price:  # 如果当前价小于带单价： trade_amount = 初始设定值
                    values["trade_amount"] = values["trade_amount_bak"]
                    values["sell_value"] = 0

            # 带单计算：sell_value
            if 'sell_valuex' in values: values["sell_value"] = values["sell_valuex"]
            elif buy_price / sell_price <= 0.99:
                bid_rate = round((1-buy_price/sell_price)*100,2)
                bid_value = round(values["buy_value"] * (1.025 - buy_price / sell_price))
                values["sell_value"] = max(values["buy_value"] + max(20, bid_value * 2), values["sell_value"] if "sell_value" in values else 0)
                if bid_rate >= 1.5:
                    print(f"{coin} 价差：{bid_rate}% {bid_value}", "buy_value", values["buy_value"], "sell_value", values["sell_value"])
            elif not "sell_value" in values or values["sell_value"] < values["buy_value"] + 10:
                if values["trade_amount"] < 10: values["sell_value"] = values["buy_value"] + 12
                else: values["sell_value"] = round(values["buy_value"] + values["trade_amount"] * 1.98, 0)
                # print(values)
            
            # 虚拟余额
            if int(symbol_balance * buy_price) <= 5: zero_coin += coin + " "
            if virtual_balance_enable != True: values['vb'] = 0
            if 'vb' in values: values["virtual_balance"] = values['vb'] / buy_price
            elif not "virtual_balance" in values:
                virtual_balance = max(0, (values["buy_value"] + values["trade_amount"] / 1.28) / buy_price - symbol_balance)
                if virtual_balance * buy_price < values["trade_amount"]: virtual_balance = 0
                keep_value = values["kv"] + values["trade_amount"] / 1.77 if "kv" in values else values["trade_amount"] * 1.99
                if symbol_balance * buy_price < keep_value: virtual_balance -= keep_value / buy_price - symbol_balance
                values["virtual_balance"] = max(virtual_balance, 0)
            virtual_balance = values["virtual_balance"] if values["virtual_balance"] * buy_price > values["trade_amount"] else 0
            virtual_buy_value = virtual_balance * buy_price
            symbol_balance += virtual_balance

            # 计算账户余额的价值
            buy_value = round(symbol_balance * buy_price, values["priceScale"])
            sell_value = round(symbol_balance * sell_price, values["priceScale"])
            sum_buy_value += buy_value; sum_spot_value += buy_value - virtual_buy_value

            # 先尝试关闭最有利可图的带单
            profit_rate = 1.055
            symbol_order = values["top"] if "top" in values else 9999
            if symbol_order <= 5: profit_rate = 1.012
            elif symbol_order <= 20: profit_rate = 1.023
            elif symbol_order <= 100: profit_rate = 1.031
            elif symbol_order <= 300: profit_rate = 1.041
            elif symbol_order <= 500: profit_rate = 1.051
            elif symbol_order <= 1000: profit_rate = 1.061
            elif symbol_order <= 3000: profit_rate = 1.081
            elif symbol_order <= 5000: profit_rate = 1.111
            elif lead_price > 0: print(f"{symbol} top", symbol_order); err_coin += coin + " "
            elif order_balance > 0: err_coin += coin + " "
            if "profit_rate" in values and values["profit_rate"] >= profit_rate: profit_rate = values["profit_rate"] # and values["profit_rate"] > profit_rate
            success, min_buy_price, max_buy_price = close_most_profitable_order(order_list, symbol, buy_price, profit_rate)
            # 0-正常持币，1-止盈清仓：等待全部订单获利，2-止盈清仓：1+add带单，3-add带单，4-立刻清仓
            if not "st" in values: values["st"] = 1 # if sell_price < lead_price else 0
            if values["st"] == 4: # 立刻清仓
                if saving_balance > 0: # 赎回理财
                    result = savings_redeem(api_key, api_secret, api_passphrase, "flexible", product_id, saving_balance)
                    if result and result['code'] == '00000': print(f"赎回 {saving_balance} {coin} 成功: {result['msg']}")
                    else: print(f"赎回 {saving_balance} {coin} 失败: {result}")
                elif order_balance > 0: # 卖出带单
                    for order in order_list:
                        if order['symbol'] == symbol:
                            success, result = close_tracking_order_v2(api_key, api_secret, api_passphrase, symbol, [order['trackingNo']])
                            if success: print(f"成功卖出: {symbol} {json.dumps(result, separators=(',', ':'))}"); time.sleep(0.5)
                elif buy_value - virtual_buy_value >= 1: # 卖出现货
                    quantity = truncate(symbol_balance - virtual_balance, values['quantityScale'], 'float')
                    response = spot_place_order(api_key, api_secret, api_passphrase, symbol, 'sell', 'market', 'gtc', quantity)
                    if response != None and response['code'] == '00000':
                        print(f"卖出 {coin}，数量为 {quantity}，成交价为 {buy_price} USDT")
                    else: print(f"卖出 {coin} {response}")
                if spot_trace_enable(spot_trace_list, symbol) != 'delete': # 关闭带单
                    response = spot_trader_symbols(api_key, api_secret, api_passphrase, [symbol], "delete")
                continue
            if values["st"] in (1,2): lead_price = min(lead_price, max_buy_price) if max_buy_price > 0 else 0
            if 0 < lead_price < sell_price < lead_price * 2: over_coin += coin + " "
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"{i}. {coin}  价格:{truncate(sell_price,10)}  余额 buy:{int(buy_value-virtual_buy_value)}{'+'+str(int(virtual_buy_value)) if virtual_balance>0 else''} sell:{int(sell_value)}  min:{truncate(min_buy_price,10)} max:{truncate(max_buy_price,10)} st:{values['st']} cnt:{order_count}"),  # 数量小数位数：{precision}
            if success: buy_value -= values["trade_amount"]; sleep_time = 5; sold_coin += coin + " "
            if sell_price < min_buy_price * 0.94:
                print(f"{symbol} 购入价：{truncate(min_buy_price,10)}  当前价：{truncate(sell_price,10)}  差价：{int(100-round(sell_price/min_buy_price,2)*100)}%  建议补仓！！！")
                if usdt_balance + usdt_flexible > 200 and sell_price < lead_price and virtual_balance > 0 and spot_trace_enable(spot_trace_list, symbol) != "":
                    values["virtual_balance"] = max(0, virtual_balance - values["trade_amount"] / buy_price)
                    virtual_balance = values["virtual_balance"]
                    virtual_buy_value = virtual_balance * buy_price; sell_value -= virtual_buy_value
                    print("virtual_balance", virtual_balance, "virtual_buy_value", virtual_buy_value)
                else: print(f"usdt:{usdt_balance + usdt_flexible} sell_price: {truncate(sell_price,10)} lead_price: {truncate(lead_price,10)} vb: {virtual_balance}")
            
            # BGB有launchpool
            if symbol == "BGBUSDT" and sell_value > 5:
                if buy_value > values['sell_value'] * 1.2: continue
                if sell_value < values['sell_value'] * 0.8 and values['buy_value'] > 500: continue

            # 如果价值低于买入价值，则买入指定数量的币种
            if sell_price > 0 and sell_value < values['buy_value']:
                # if buy_price / sell_price <= 0.97:
                #     print(f"买卖价差: {round(buy_price/sell_price,2)} <= 0.97 暂不买入！")
                #     continue
                # 检查USDT余额
                redeem_usdt = False; trade_amount = values["trade_amount"]
                if symbol in ["ETHUSDT", "BTCUSDT"] and sell_price < min_buy_price * 0.985 and usdt_balance < trade_amount and usdt_flexible > 1000:
                    redeem_usdt = True; keep_step = usdt_keep_step
                if (auto_redeem_usdt or redeem_usdt) and usdt_balance < keep_step and usdt_flexible >= keep_step:
                    usdt_balance += keep_step; usdt_flexible -= keep_step
                    result = savings_redeem(api_key, api_secret, api_passphrase, "flexible", usdt_product_id, keep_step)
                    if result and result['code'] == '00000': print(f"赎回 {keep_step} USDT 成功: {result['msg']}")
                    else: print(f"赎回 {keep_step} USDT 失败: {result}")
                if usdt_balance < trade_amount: continue
                action = None
                if spot_trader_enable: # 开启带单
                    if lead_price > 0 and sell_price > lead_price: action = 'delete'
                    elif sell_price < lead_price * 0.5: action = 'add'
                    elif sell_price < max_buy_price * 0.6: action = 'add'
                    elif sell_price < min_buy_price * 0.93: action = 'add'
                    elif min_buy_price > 0 and sell_price > min_buy_price * 0.985: action = "add" if values["st"] in (2,3) else "delete"
                    elif sell_price < lead_price: action = 'add'
                    # elif min_buy_price > 0: action = 'delete'
                    if action:
                        if action == "add" and buy_price / sell_price <= 0.98:
                            print(f"买卖价差: {round(buy_price/sell_price,2)} <= 0.98 暂不买入！")
                            continue
                        print(time.strftime("%Y-%m-%d %H:%M:%S"), f'{action}:带单', symbol, sell_price, min_buy_price, max_buy_price, lead_price)
                        if spot_trace_enable(spot_trace_list, symbol) != action:
                            response = spot_trader_symbols(api_key, api_secret, api_passphrase, [symbol], action)
                            if response != None and response['code'] == '00000': success = True
                if action != "add" and values["st"] != 0: continue
                if action == "add" and order_time > time.time(): time.sleep(order_time - time.time())
                elif success: time.sleep(7)
                # 买入现货V2
                quantity = trade_amount
                usdt_balance -= trade_amount
                response = spot_place_order(api_key, api_secret, api_passphrase, symbol, 'buy', 'market', 'gtc', quantity)
                if response != None and response['code'] == '00000':
                    if virtual_balance > 0: virtual_balance -= trade_amount / buy_price / 10
                    print(f"买入 {coin}，数量为 {quantity}，成交价为 {sell_price} USDT")
                else:
                    print(f'买入 {quantity} 失败:', response); err_coin += coin + " "
                order_time = time.time() + 11

            # 如果价值高于卖出价值，则卖出指定数量的币种
            elif buy_value >= values['sell_value']:
                # 先尝试关闭最有利可图的带单
                # success, min_buy_price, max_buy_price = close_most_profitable_order(order_list, symbol, buy_price, profit_rate)
                # 如果关闭带单成功，则重新获取带单列表，如果失败，则卖出现货
                if success != False:
                    sleep_time = 5
                    while success != False:
                        if buy_price > min_buy_price * 1.3: time.sleep(1)
                        elif buy_price > min_buy_price * 1.2: time.sleep(2)
                        elif buy_price > min_buy_price * 1.1: time.sleep(5)
                        elif buy_price > min_buy_price * 1.05: time.sleep(11)
                        else: time.sleep(15)
                        response = get_spot_market_tickers(api_key, api_secret, api_passphrase, symbol)
                        if response and response['code'] == '00000': buy_price = float(response['data'][0]['bidPr'])
                        success, min_buy_price, max_buy_price = close_most_profitable_order(success, symbol, buy_price, profit_rate)
                else:
                    # else:
                    # 计算卖出金额及数量
                    trade_amount = buy_value - values['sell_value'] + values["trade_amount"]
                    if sell_price < min_buy_price * 0.94: trade_amount += values["trade_amount"] * 0.75
                    quantity = truncate(trade_amount / buy_price, values['quantityScale'], 'float')
                    # 判断余额是否够卖
                    if (symbol_balance - order_balance) * buy_price < trade_amount or trade_amount < 5.20: continue
                    print(f'{symbol} bv: {values["buy_value"]}, sv: {values["sell_value"]}, ta: {trade_amount}')

                    # 卖出虚拟余额
                    if virtual_balance > 0 and lead_price > sell_price: # and symbol_balance - order_balance - virtual_balance < quantity:
                        virtual_balance = virtual_balance - quantity if virtual_balance >= quantity else 0
                        values["virtual_balance"] = virtual_balance if virtual_balance > 0 else 0
                        print(f"卖出虚拟余额 {coin}，金额为 {trade_amount}，成交价为 {buy_price} USDT")
                        continue
                    
                    # 现货不够卖，则全部卖出
                    if symbol_balance - order_balance - virtual_balance < quantity:
                        quantity = truncate(symbol_balance - order_balance - virtual_balance, values['quantityScale'], 'float')
                        if virtual_balance > 0: virtual_balance -= values["trade_amount"] / buy_price
                    elif virtual_balance * buy_price + values["trade_amount"] > values['sell_value']:
                        if virtual_balance > 0: virtual_balance -= values["trade_amount"] / buy_price
                    elif virtual_balance > 0: virtual_balance -= values["trade_amount"] / buy_price / 2
                    
                    # 如果有活期理财宝余额，则先赎回活期理财宝到现货
                    redeem_quantity = 0
                    if saving_balance > 0: # asset_balance < quantity and
                        saving_scale = len(str(saving_balance).split(".")[1]) if "." in str(saving_balance) else 0
                        quantity = truncate(quantity, min(values['quantityScale'], saving_scale), 'float')
                        redeem_quantity = min(quantity, saving_balance)
                        if redeem_quantity == 0: redeem_quantity = saving_balance
                        result = savings_redeem(api_key, api_secret, api_passphrase, "flexible", product_id, redeem_quantity)
                        if result and result['code'] == '00000': print(f"赎回 {coin} 数量 {redeem_quantity} 成功: {result['msg']}")
                        else: print(f"赎回 {coin} 数量 {redeem_quantity} 金额 {trade_amount} 失败: {result}")
                        time.sleep(5)
                    # 卖出现货V2
                    sold_coin += coin + " "
                    response = spot_place_order(api_key, api_secret, api_passphrase, symbol, 'sell', 'market', 'gtc', quantity)
                    if response != None and response['code'] == '00000':
                        print(f"卖出 {coin}，数量为 {quantity}，成交价为 {buy_price} USDT")
                    else:
                        response = spot_place_order(api_key, api_secret, api_passphrase, symbol, 'sell', 'market', 'gtc', int(trade_amount))
                        if response != None and response['code'] == '00000':
                            print(f"卖出 {coin}，金额为 {trade_amount}，成交价为 {buy_price} USDT")
                        else:
                            print(f'卖出 {coin}，数量 {quantity} 金额 {trade_amount} 失败:', response['msg'])
                            err_coin += coin + " "
            elif (asset_balance - order_balance) * buy_price > 5:
                earn = values["earn"] if "earn" in values else 0.01
                if earn <= 0: continue
                if not coin in savings_product: # 获取理财产品信息
                    result = get_savings_product(api_key, api_secret, api_passphrase, coin)
                    savings_product[coin] = result["data"] if result != None and result["code"] == "00000" else []
                minStepVal = values["minStepVal"] if "minStepVal" in values else 2 / buy_price
                saving_scale = values['quantityScale']
                if saving_balance > 0: saving_scale = len(str(saving_balance).split(".")[1]) if "." in str(saving_balance) else 0
                spot_quantity = truncate(asset_balance - order_balance - earn / buy_price, saving_scale, 'float')
                spot_amount = round(spot_quantity * buy_price, 2)
                if coin in savings_product and spot_quantity > minStepVal: # 理财申购
                    for product in savings_product[coin]:
                        if product['periodType'] == "flexible" and product["status"] == "in_progress":
                            result = savings_subscribe(api_key, api_secret, api_passphrase, "flexible", product['productId'], spot_quantity)
                            print(f"申购 {coin} 数量 {spot_quantity} 金额 {spot_amount} 结果: {result} {product}")
                            break
            if values["virtual_balance"] > virtual_balance:
                print("virtual_balance>", values["virtual_balance"], ">", virtual_balance)
                values["virtual_balance"] = virtual_balance if virtual_balance > 0 else 0
            elif values["virtual_balance"] < virtual_balance:
                print("virtual_balance<", values["virtual_balance"], "<", virtual_balance)
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S"), symbol, f"Exception:", str(e))
        
        time.sleep(0.01)

    print(time.strftime("%Y-%m-%d %H:%M:%S"), f"sum_buy_value", round(sum_buy_value), "sum_spot_value", round(sum_spot_value), "usdt", round(usdt_balance + usdt_flexible))
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "sold_coin", sold_coin, "err_coin", err_coin, "over_coin", over_coin, "zero_coin", zero_coin)
    
    # 休息时间
    time.sleep(sleep_time)
