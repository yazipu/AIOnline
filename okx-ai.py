# -*- coding: utf-8 -*-
# https://www.okx.com/docs-v5/zh/#overview
import requests, json, hashlib, hmac, time, base64, datetime

import okx
from okx.api import API as OKXApi
from paux.param import to_local
import urllib.parse as up

virtual_balance_enable = False # 是否启用虚拟余额
usdt_keep = 500     # 保持现货 USDT 余额
keep_step = 500     # 每次赎回 USDT 金额
spot_holding = 0    # 现货：0-正常持币，1-逐渐减仓，4-立刻清仓
copy_holding = 0    # 带单：0-正常持币，1-逐渐减仓，4-立刻清仓
spot_position = 1   # 现货仓位：1-100%仓位，0.9-90%仓位，1.1-110%仓位
copy_position = 1   # 带单仓位：1-100%仓位，0.9-90%仓位，1.1-110%仓位

# 设置API密钥和密钥、操作配置
flag = "1"          # 实盘:0 , 模拟盘:1
###
# 模拟交易key
# flag = "1"
# api_key = 'xxx-xxx'
# api_secret = '私钥'
# api_passphrase = '口令'
###
###
# 真实
flag = "0"
api_key = 'xxx-xxx'
api_secret = '私钥'
api_passphrase = '口令'
###
###########用户账户设置##############
# 用户角色
API_ROLE = ["普通用户","带单者","跟单者"]
DAI_DAN_ZHE_ROLE = 1 # 带单者
# # 账户层级
# ACCOUNT_LEVEL = ["简单交易模式","单币种保证金模式","跨币种保证金模式","组合保证金模式"]
# # API key权限
# API_PERM = {"read_only":"读取","withdraw":"交易","trade":"提币"}
# def apiKeyPerm(perm:str):
#     permSplit = perm.split(",")
#     permStr = ""
#     for perm in permSplit:
#         if permStr != "":
#             permStr = permStr + ","T
#         permStr = permStr + API_PERM[perm]
#     return permStr
#####################

# 设置要检测的币种和相应的价值判断（trader_mode(交易模式):lead(带单)、copy(跟单)、ordinary(普通)默认值）
"""
lead_price(带单金额上限): 币金额达到设置上限则交易优先级 lead_price(达到上线则现货交易)
"""
symbols = {
    # 平台币
    'OKBUSDT': { 'lead_price': 888, 'buy_value': 700, 'trade_amount': 23, 'profit_rate': 1.015, 'top': 28 },

    # 带单交易对
    'BTCUSDT': { 'lead_price': 880000, 'buy_value': 5050, 'trade_amount': 60, 'profit_rate': 1.012, 'top': 1,'st':0 },
    'ETHUSDT': { 'lead_price': 33000, 'buy_value': 2980, 'trade_amount': 40, 'profit_rate': 1.012, 'top': 2,'st':0 },

    'SOLUSDT': { 'lead_price': 888, 'buy_value': 420, 'trade_amount': 23, 'profit_rate': 1.0125, 'top': 5 },
    'XRPUSDT': { 'lead_price': 8.8, 'buy_value': 380, 'trade_amount': 23, 'profit_rate': 1.0125, 'top': 6,'vb':0 },

    'DOGEUSDT': { 'lead_price': 8.8, 'buy_value': 410, 'trade_amount': 23, 'profit_rate': 1.015, 'top': 10 },
    'SHIBUSDT': { 'lead_price': 0.0066, 'buy_value': 380, 'trade_amount': 23, 'top': 16 },
    
    'ARBUSDT': { 'lead_price': 88.8, 'buy_value': 760, 'trade_amount': 23, 'top': 43 },
    'OPUSDT': { 'lead_price': 99.9, 'buy_value': 380, 'trade_amount': 23, 'top': 28 },
    'POLUSDT': { 'lead_price': 8.8, 'buy_value': 380, 'trade_amount': 23, 'top': 12 },

    'ADAUSDT': { 'lead_price': 8.8, 'buy_value': 460, 'trade_amount': 23, 'profit_rate': 1.015, 'top': 8 },
    'AVAXUSDT': { 'lead_price': 880, 'buy_value': 380, 'trade_amount': 23, 'profit_rate': 1.015, 'top': 9 },
    'BCHUSDT': { 'lead_price': 2888, 'buy_value': 410, 'trade_amount': 23, 'profit_rate': 1.015, 'top': 19 },
    'BSVUSDT': { 'lead_price': 880, 'buy_value': 380, 'trade_amount': 23, 'profit_rate': 1.022, 'top': 42 },
    'DOTUSDT': { 'lead_price': 88, 'buy_value': 400, 'trade_amount': 23, 'top': 11 },
    'LTCUSDT': { 'lead_price': 888, 'buy_value': 400, 'trade_amount': 23, 'profit_rate': 1.015, 'top': 17 },
    'TONUSDT': { 'lead_price': 88, 'buy_value': 380, 'trade_amount': 23, 'profit_rate': 1.025, 'top': 15 },

    'FILUSDT': { 'lead_price': 66, 'buy_value': 380, 'trade_amount': 23, 'top': 34 },
    'LINKUSDT': { 'lead_price': 99, 'buy_value': 380, 'trade_amount': 23, 'top': 14 },

    'JSTUSDT': { 'lead_price': 0.88, 'buy_value': 380, 'trade_amount': 23, 'profit_rate': 1.025, 'top': 172 },
    'TRXUSDT': { 'lead_price': 0.88, 'buy_value': 580, 'trade_amount': 33, 'top': 13,'vb':0 },

    'APTUSDT': { 'lead_price': 88, 'buy_value': 380, 'trade_amount': 23, 'top': 31 },
    'LDOUSDT': { 'lead_price': 88, 'buy_value': 400, 'trade_amount': 23, 'top': 38 },
    'SUIUSDT': { 'lead_price': 88, 'buy_value': 380, 'trade_amount': 23, 'top': 50 },
    'WLDUSDT': { 'lead_price': 88, 'buy_value': 380, 'trade_amount': 23, 'profit_rate': 1.041, 'top': 144 },

    # 无带单交易对
    # 'WINUSDT': { 'buy_value': 380, 'trade_amount': 23, 'profit_rate': 1.041, 'top': 375,'vb':0 },

    # ST
    # 'AGIXUSDT': { 'lead_price': 0.001, 'buy_value': 380, 'trade_amount': 23, 'num_dp': 4, 'top': 132,'st':4 },

    # 下架交易对
    # 'YFIIUSDT': { 'lead_price': 100, 'buy_value': 0, 'sell_valuex': 280, 'trade_amount': 23, 'profit_rate': 1.041, 'top': 627,'st':4 },
    
}

# 截断小数，不四舍五入
def truncate(number, decimal_places, return_type="string"):
    factor = 10 ** decimal_places
    truncated_number = int(number * factor) / factor
    if truncated_number == int(truncated_number): truncated_number = int(truncated_number)
    if return_type != "string": return truncated_number
    return f'{truncated_number:.{decimal_places}f}'.rstrip('0').rstrip('.')

# 交易对格式转换（将配置交易对转换成okx平台交易对，便于多平台兼容）
def convertOkxPair(symbols, spot_position = 1, copy_position = 1):
    _tmp = {}
    for symbol,values in symbols.items():
        trading_rate = copy_position if "lead_price" in values else spot_position
        if "lead_price" in values and trading_rate < 1: values["lead_price"] *= trading_rate
        values["buy_value"] = round(values["buy_value"] * trading_rate)
        values["trade_amount"] = max(round(values["trade_amount"] * trading_rate), 11)
        if "sell_value" in values: values["sell_value"] = round(max(values["sell_value"] * trading_rate, values["buy_value"] + values["trade_amount"] * 1.99))
        if "sell_valuex" in values: values["sell_valuex"] = round(max(values["sell_valuex"] * trading_rate, values["buy_value"] + values["trade_amount"] * 1.99))
        _tmp[symbol[:-4] + "-" + symbol[-4:]] = values
    return _tmp

# okxAPI的替补
class OKXApiSub():
    API_URL = 'https://www.okx.com'

    def __init__(self,key, secret, passphrase, flag):
        self._api_key = key
        self._api_secret = secret
        self._api_passphrase = passphrase
        self._flag = flag

    # 将字典中不为空的取出
    def get_params_no_empty(self, params):
        if params == "": return {}
        params_no_empty = {}
        for k, v in params.items():
            if v not in ['', [], {}, None]: params_no_empty[k] = v
        return params_no_empty

    # 构造请求头 https://www.okx.com/cn/web3/build/docs/devportal/rest-authentication
    def get_okx_headers(self, method, path, body=""):
        timestamp = datetime.datetime.utcnow().isoformat("T", "milliseconds") + 'Z'

        # 构建待签名字符串
        message = f'{timestamp}{method.upper()}{path}{body}'

        # 计算出签名
        message = str(timestamp) + str.upper(method) + path + body
        mac = hmac.new(bytes(self._api_secret, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        sign = base64.b64encode(d)

        headers = {}
        headers['Content-Type'] = 'application/json'
        headers['OK-ACCESS-KEY'] = self._api_key
        headers['OK-ACCESS-SIGN'] = sign
        headers['OK-ACCESS-TIMESTAMP'] = str(timestamp)
        headers['OK-ACCESS-PASSPHRASE'] = self._api_passphrase
        headers['x-simulated-trading'] = self._flag

        return headers
    
    def _request(self, method: str = "", path: str = "", params: str = ""):
        try:
            body = ''
            params_no_empty = self.get_params_no_empty(params)
            if method == "GET" and params_no_empty:
                query_string = up.urlencode(params_no_empty)
                if query_string: path = path + "?" + query_string
            elif method == 'POST' and params_no_empty : body = json.dumps(params_no_empty)

            headers = self.get_okx_headers(method, path, body)
            response = requests.request(method, self.API_URL + path, headers=headers, data=body, timeout=(20,60))

            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取{path}失败: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
        return None
    
    def get(self, path: str = "", params: str = "",): return self._request('GET', path, params)
    def post(self, path: str = "", params: str = ""): return self._request('POST', path, params)
        
    ## 交易账户(Account)
    # 查看账户配置
    def account_get_config(self): return self.get("/api/v5/account/config")
    # 获取交易账户中资金余额信息
    def account_get_balance(self, ccy:str = ''): return self.get('/api/v5/account/balance', to_local(locals()))
    
    ## 行情数据(Market)
    # 获取所有产品行情信息
    def market_get_tickers(self,instType:str):return self.get("/api/v5/market/tickers", to_local(locals()))
    # 获取单个产品行情信息
    def market_get_ticker(self,instId:str):return self.get("/api/v5/market/ticker", to_local(locals()))

    ##资金账户(FundingAccount)
    # 资金划转
    def fundingAccount_set_transfer(self, ccy: str, amt: str, from_:str, to: str, type: str = '', subAcct: str = '',
                     loanTrans: bool = '', omitPosRisk: str = '', clientId: str = ''):
        data = to_local(locals())
        data['from'] = data['from_']
        del data['from_']
        return self.post("/api/v5/asset/transfer", data)
    def asset_get_balances(self,ccy:str=''):return self.get("/api/v5/asset/balances", to_local(locals()))

    ##跟单(CopyTrade)
    # 交易员获取当前带单
    def copyTrade_get_current_subpositions(self, instType:str='', instId: str = '', after: str = '', before: str = '', limit: str = ''):
        return self.get('/api/v5/copytrading/current-subpositions', to_local(locals()))
    # 交易员获取历史带单
    def copyTrade_get_subpositions_history(self, instType:str='', instId: str = '', after: str = '', before: str = '', limit: str = ''):
        return self.get('/api/v5/copytrading/subpositions-history', to_local(locals()))
    # 交易员平仓
    def copyTrade_set_close_subposition(self, subPosId: str, instType:str='' , tag: str = ''):
        return self.post('/api/v5/copytrading/close-subposition', to_local(locals()))

# 查找并关闭盈利最多的带单
def close_most_profitable_order(orders, symbol, price, rate = 1.0125):    
    # 初始化最大盈利和对应带单
    min_buy_price = 0
    max_buy_price = 0
    min_buy_price_order = None
    if orders and len(orders) > 0:

        # 在这里遍历 orders，找到盈利最多的带单
        for order in orders:
            if order['instId'] == symbol:
                if float(order['openAvgPx']) > max_buy_price: max_buy_price = float(order['openAvgPx'])
                if float(order['openAvgPx']) < min_buy_price or min_buy_price == 0:
                    min_buy_price = float(order['openAvgPx'])
                    min_buy_price_order = order

        # 判断是否找到盈利最多的带单
        if min_buy_price_order and price > min_buy_price * rate:
            # 卖出带单
            result = okxApiSub.copyTrade_set_close_subposition(subPosId=min_buy_price_order['subPosId'], instType='SPOT')
            if result and result['code'] == "0":
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

# 赎回理财流程（赎回指定币种）
def savings_purchase_redemption(symbol, amt):    
    # 1.赎回理财指定数量币（赎回币是到资金账户）
    result = okxApi.savings.set_purchase_redempt(symbol, amt, "redempt", '')
    if result and result['code'] == '0':
        print(f"赎回成功, {amt} {symbol} 到达 资金账户")
        time.sleep(5)
        # 2.将赎回到资金账户的币划转到交易账户里（注：只有交易账户余额才能进行现货交易）
        # from=转出账户、to=转入账户（6：资金账户、18：交易账户）
        result = okxApiSub.fundingAccount_set_transfer(symbol, amt, "6", "18")
        if result and result['code'] == '0':
            print(f"划转成功，资金账户中将 {amt} {symbol} 划转到 交易账户")
            time.sleep(3)
    return result

# 初始化
symbols = convertOkxPair(symbols, spot_position, copy_position)
okxApi = OKXApi(api_key, api_secret, api_passphrase, flag=flag)
okxApiSub = OKXApiSub(api_key, api_secret, api_passphrase, flag=flag)
version = okx.__version__
print(time.strftime("%Y-%m-%d %H:%M:%S"), f"python-okx 当前版本 {version}")

# 现货跟单角色类型（与用户角色对应）
spotRoleType = 0
result = okxApiSub.account_get_config()
if result and result['code'] == "0":
    spotRoleType = int(result['data'][0]['spotRoleType'])
    # print("当前用户配置：",result['data'][0])
    # print("当前用户角色：",API_ROLE[int(result['data'][0]['roleType'])])
    print("当前合约跟单角色：",API_ROLE[int(result['data'][0]['roleType'])])
    print("当前现货跟单角色：",API_ROLE[spotRoleType])
    # print("现货带单设置币种列表：",result['data'][0]['spotTraderInsts'])
else:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "获取用户配置失败")

# 获取现货交易对精度
# https://www.okx.com/docs-v5/zh/#public-data-rest-api-get-instruments
result = okxApi.public.get_instruments(instType="SPOT")
if result and result["code"] == "0":
    spot_symbols = result["data"]
    for symbol, values in symbols.items():
        values["priceScale"] = values["num_dp"] if "num_dp" in values else 0
        values["quantityScale"] = values["num_dp"] if "num_dp" in values else 0
        for spot_symbol in spot_symbols:
            if symbol == spot_symbol["instId"]:
                if "." in spot_symbol["tickSz"]: values["priceScale"] = len(spot_symbol["tickSz"].split(".")[1])
                if "." in spot_symbol["lotSz"]: values["quantityScale"] = len(spot_symbol["lotSz"].split(".")[1])

# 每10分钟执行一次检测和交易操作
while True:
    try:
        i = 0
        
        # 获取理财信息
        retry = 0
        quantity = 0
        savings_list = []
        for page in range(1, 100):
            # 模拟交易中暂时不可用
            if flag == "1": break
            result = okxApi.savings.get_balance()
            if result and result["code"] == "0":
                data = result["data"]
                savings_list.extend(data)
                break
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S"), f"获取【活期简单赚币】资产失败: {result}")
                retry = retry + 1
                if retry > 30: exit()
                else: time.sleep(30)
                continue
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "当前【活期简单赚币】资产数量", len(savings_list))    
        
        # 当日带单和历史带单整合
        today_order_list = []
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # 获取带单列表
        retry = 0
        min_id = ""
        order_list = []    
        for page in range(1, 1000):
            # 非带单者不获取带单信息
            if str(spotRoleType) != str(DAI_DAN_ZHE_ROLE): break
            result = okxApiSub.copyTrade_get_current_subpositions(instType='SPOT', after=min_id, limit=500)
            # print("获取当前带单列表:",result)
            if result and result["code"] == "0":
                data = result["data"]
                if len(data) > 0: min_id = data[-1]["subPosId"]
                order_list.extend(data)
                for obj in data:
                    if today == datetime.datetime.fromtimestamp(int(obj['openTime'])/1000).strftime("%Y-%m-%d"):
                        today_order_list.append(obj)
                    else: break
                if len(data) < 500: break
                else: time.sleep(0.1)
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S"), f"获取【带单】失败: {result}")
                retry = retry + 1
                if retry > 30: exit()
                else: time.sleep(20)
                continue
        # print(time.strftime("%Y-%m-%d %H:%M:%S"), "当前带单数量:", len(order_list))

        # 历史带单查看当日带单量记录
        retry = 0
        min_id = ""
        order_list_history = []
        for page in range(1, 1000):
            # 非带单者不获取带单信息
            if str(spotRoleType) != str(DAI_DAN_ZHE_ROLE): break
            isEnd = False
            result = okxApiSub.copyTrade_get_subpositions_history(instType='SPOT', after=min_id, limit=100)   
            # print("获取历史带单列表:",result)
            if result and result["code"] == "0":
                data = result["data"]
                if len(data) > 0: min_id = data[-1]["subPosId"]
                # order_list_history.extend(data)
                for obj in data:
                    if today == datetime.datetime.fromtimestamp(int(obj['openTime'])/1000).strftime("%Y-%m-%d"):
                        today_order_list.append(obj)
                    else: 
                        isEnd = True 
                        break
                if isEnd == True: break
                if len(data) < 100: break
                else: time.sleep(0.1)
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S"), f"获取历史【带单】失败: {result}")
                retry = retry + 1
                if retry > 30: exit()
                else: time.sleep(20)
                continue

        # 只有带单者才需要输出每日买入次数    
        if str(spotRoleType) == str(DAI_DAN_ZHE_ROLE):
            print(time.strftime("%Y-%m-%d %H:%M:%S"), "当日【买入】次数", len(today_order_list))

        # 资金 -> 现货
        result = okxApiSub.asset_get_balances()
        if result and result['code'] == '0' and len(result['data']) > 0:
            asset_balances = result['data']
            for balance in asset_balances:
                # {'availBal': '0.00000000251', 'bal': '0.00000000251', 'ccy': 'BTC', 'frozenBal': '0'}
                if float(balance['availBal']) > 0 and not balance['ccy'] in ["AGIX", "GAL", "MATIC"]:
                    coin = balance['ccy']
                    availBal = balance['availBal']
                    result = okxApiSub.fundingAccount_set_transfer(coin, availBal, "6", "18")
                    print(f'资金->现货: {coin}: {availBal}')

        # 获取交易账户中的余额
        balances = {}
        try:
            result = okxApiSub.account_get_balance()
            if result and result['code'] == '0' and len(result['data']) > 0:
                balances = result['data'][0]['details']
            else:
                print('获取账户余额失败:', result)
                time.sleep(30)
                continue
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"获取余额失败 Exception:", str(e))
            time.sleep(30)
            continue
        
        # 500 USDT+资金的币种权益（币种权益 = 该币种可用余额 + 占用余额 + 期权市值） 和 每日（指当天0～24小时范围）买入次数<=500次
        usdt_productId = ""
        usdt_balance = 0
        usdt_flexible = 0
        # USDT 现货余额
        for balance in balances:
            if balance['ccy'] == "USDT":
                usdt_balance = round(float(balance['cashBal']), 6)
                # print(balance)
            elif balance['ccy'] != "USDC":
                exist = False
                for symbol, values in symbols.items():
                    if balance['ccy'] == symbol[:-5]: exist = True; break
                if not exist: print(balance['ccy'], "余额", round(float(balance['cashBal']), 2), "未配置！")
        # USDT 活期理财余额
        for saving in savings_list:
            if saving['ccy'] == "USDT":
                usdt_flexible = round(float(saving['amt']), 6)
            elif saving['ccy'] != "USDC":
                exist = False
                for symbol, values in symbols.items():
                    if saving['ccy'] == symbol[:-5]: exist = True; break
                if not exist: print(saving['ccy'], "余额", round(float(saving['amt']), 2), "未配置！")
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"USDT:{usdt_balance} 活期:{usdt_flexible}")
        if usdt_balance < usdt_keep and usdt_flexible >= keep_step:
            # 赎回指定数量币
            result = savings_purchase_redemption("USDT", keep_step)
            if result and result['code'] != '0':
                print(f"赎回 {keep_step} USDT 失败: {result}") 
                time.sleep(30)
                continue
        elif usdt_balance > usdt_keep * 3:
            lend_usdt = int(usdt_balance - usdt_keep * 2)
            result = okxApiSub.fundingAccount_set_transfer("USDT", lend_usdt, "18", "6")
            if result and result["code"] == "0":
                result = okxApi.savings.set_purchase_redempt("USDT", lend_usdt, "purchase", '0.01')
                print(f"申购 {lend_usdt} USDT : {result}")
        # elif usdt_balance < 500 and str(spotRoleType) == str(DAI_DAN_ZHE_ROLE):
        #    print(f"现货带单员交易账户不足500USDT（币种权益）。此时交易员可以继续正常交易，但是跟单员不能成功跟随此次带单")

        ticker_list = {}
        ticker_time = 1500 # 间隔时间
        spot_isolated_times = 0
        
        # 计算带单数量、总额及盈利
        ticker_list = okxApiSub.market_get_tickers(instType="SPOT")
        if ticker_list and ticker_list["code"] == "0":
            ticker_list['rtime'] = int(time.time() * 1000) + ticker_time
            order_amount = 0; order_profit = 0; order_symbol = set()
            for order in order_list:
                order_amount += float(order["availSubPos"]) * float(order['openAvgPx'])
                buy_price = next((float(data['bidPx']) for data in ticker_list['data'] if data["instId"] == order["instId"]), 0)
                if buy_price > 0: order_profit += float(order["availSubPos"]) * (buy_price - float(order['openAvgPx']))
                if not order["instId"] in order_symbol: order_symbol.add(order["instId"])
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"当前带单数量：{len(order_list)} 币种：{len(order_symbol)} 总额：{round(order_amount,2)} 盈利：{round(order_profit,2)}")
            time.sleep(3)
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "Exception:", str(e))
        time.sleep(60)
        continue
    
    sleep_time = 60; sum_buy_value = 0; sum_spot_value = 0; sold_coin = err_coin = over_coin = zero_coin = ""; order_time = time.time()
    for symbol, values in symbols.items():
        try:
            i = i + 1
            coin = symbol[:-5]
            asset_balance = 0
            order_balance = 0
            saving_balance = 0
            for balance in balances:
                if balance['ccy'] == coin:
                    asset_balance = float(balance['cashBal']) # 现货余额
                    order_balance = float(balance['spotIsoBal']) # 带单余额
                    if asset_balance == int(asset_balance): asset_balance = int(asset_balance)
                    if order_balance == int(order_balance): order_balance = int(order_balance)
                    break
            for saving in savings_list:
                if saving['ccy'] == coin:
                    saving_balance = float(saving['amt'])
                    if saving_balance == int(saving_balance): saving_balance = int(saving_balance)
                    break
            order_count = 0
            for order in order_list:
                if order['instId'] == symbol:
                    order_count += 1
            # 现货余额 + 理财余额 + 带单余额
            symbol_balance = asset_balance + saving_balance + order_balance
            if "lead_only" in values: symbol_balance = order_balance
            elif "spot_only" in values: symbol_balance = asset_balance

            # 获取所有币种价格
            buy_price = 0; sell_price = 0
            if not "rtime" in ticker_list or ticker_list['rtime'] < int(time.time() * 1000):
                result = okxApiSub.market_get_tickers(instType="SPOT")
                if result and result["code"] == "0": 
                    ticker_list = result
                    ticker_list['rtime'] = int(time.time() * 1000) + ticker_time
                else:
                    print('获取价格失败:', result)
                    continue
            for _ticker in ticker_list['data']:
                if _ticker["instId"] == symbol:
                    buy_price = float(_ticker['bidPx'])
                    sell_price = float(_ticker['askPx'])
                    break
                
            # 虚拟余额
            if buy_price <= 0 or sell_price <= 0: print(f"{i}. {coin} 获取价格失败!!!"); err_coin += coin + " "; continue
            if int(symbol_balance * buy_price) <= 11: zero_coin += coin + " "
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
            symbol_balance += virtual_balance

            # 计算账户余额的价值
            buy_value = round(symbol_balance * buy_price, values["priceScale"])
            sell_value = round(symbol_balance * sell_price, values["priceScale"])
            sum_buy_value += buy_value; sum_spot_value += buy_value - virtual_buy_value

            # 带单计算：trade_amount
            if not "trade_amount_bak" in values: values["trade_amount_bak"] = values["trade_amount"]
            lead_price = values["lead_price"] if "lead_price" in values else 0
            if lead_price > 0 and values["buy_value"] >= 100 and not 'sell_valuex' in values: # 是否开启带单
                if buy_price > lead_price * 1.02: # 如果当前价大于带单价*1.02：trade_amount = max(当前价*0.02, 10)
                    values["trade_amount"] = max(int(values["buy_value"] * 0.02), 21)
                    values["sell_value"] = 0
                elif sell_price < lead_price:  # 如果当前价小于带单价： trade_amount = 初始设定值
                    values["trade_amount"] = values["trade_amount_bak"]
                    values["sell_value"] = 0
            
            # 计算：sell_value
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
            
            # 0-正常持币，1-止盈清仓：开单间隔1.2%，2-max_buy_value止盈清仓，3-lead_price止盈清仓，4-立刻清仓
            if not "st" in values: values["st"] = copy_holding if sell_price < lead_price else spot_holding

            # 先尝试关闭最有利可图的带单
            profit_rate = 1.052
            symbol_order = values["top"] if "top" in values else 9999
            if symbol_order <= 5: profit_rate = 1.021
            elif symbol_order <= 20: profit_rate = 1.022
            elif symbol_order <= 100: profit_rate = 1.032
            elif symbol_order <= 300: profit_rate = 1.042
            elif symbol_order <= 500: profit_rate = 1.052
            elif symbol_order <= 1000: profit_rate = 1.062
            elif symbol_order <= 3000: profit_rate = 1.082
            elif symbol_order <= 5000: profit_rate = 1.111
            elif lead_price > 0: print(f"{symbol} top", symbol_order); err_coin += coin + " "
            elif order_balance > 0: err_coin += coin + " "
            if "profit_rate" in values and values["profit_rate"] >= profit_rate: profit_rate = values["profit_rate"]
            success, min_buy_price, max_buy_price = close_most_profitable_order(order_list, symbol, buy_price, profit_rate)
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"{i}. {coin}  价格:{truncate(sell_price,10)}  余额 buy:{int(buy_value-virtual_buy_value)}{'+'+str(int(virtual_buy_value)) if virtual_balance>0 else''} sell:{int(sell_value)}  min:{truncate(min_buy_price,10)} max:{truncate(max_buy_price,10)} st:{values['st']} cnt:{order_count}"),  # 数量小数位数：{precision}
            if success: buy_value -= values['trade_amount']; sleep_time = 10; sold_coin += coin + " "
            if buy_price < min_buy_price * 0.94:
                print(f"{symbol}  购入价：{round(min_buy_price,8)}  当前价：{round(buy_price,8)}  差价：{int(100-round(buy_price/min_buy_price,2)*100)}%  建议补仓！！！")
                trade_amount = values['trade_amount'] 
                if usdt_balance > trade_amount and sell_price < lead_price and values['sell_value'] > sell_value + trade_amount * 1.5:
                    sell_value = values['buy_value'] - 1
                elif usdt_balance + usdt_flexible > 200 and sell_price < lead_price and virtual_balance > 0:
                    values["virtual_balance"] = max(0, virtual_balance - values['trade_amount'] / buy_price)
                    virtual_balance = values["virtual_balance"]
                    virtual_buy_value = virtual_balance * buy_price; sell_value -= virtual_buy_value
                    print("virtual_balance", virtual_balance, "virtual_buy_value", virtual_buy_value)
                else: print(f"usdt:{usdt_balance + usdt_flexible} sell_price: {truncate(sell_price,10)} lead_price: {truncate(lead_price,10)} vb: {virtual_balance} bv:{buy_value}")

            # 订单模式（非保证金模式(现货)：cash、现货带单时：spot_isolated）
            order_mode = "cash"
            # 交易模式配置中开启带单 and 验证用户是否有带单身份
            if "lead_price" in values and str(spotRoleType) == str(DAI_DAN_ZHE_ROLE):
                lead_price = values["lead_price"]
                if values["st"] in (1,2): lead_price = min(lead_price, max_buy_price) if max_buy_price > 0 else 0
                if 0 < lead_price < sell_price < lead_price * 2: over_coin += coin + " "
                if len(today_order_list) + spot_isolated_times >= 500: order_mode = 'cash'    # 当日买入带单次数
                elif lead_price > 0 and sell_price > lead_price: order_mode = 'cash'  # 带单限额（当买入金额大于配置限额则不带单，以现货形式交易）
                elif sell_price < lead_price * 0.5: order_mode = 'spot_isolated'
                elif sell_price < max_buy_price * 0.6: order_mode = 'spot_isolated'
                elif sell_price < min_buy_price * 0.93: order_mode = 'spot_isolated'
                elif min_buy_price > 0 and sell_price > min_buy_price * 0.988: order_mode = "spot_isolated" if values["st"] in (2,3) else "cash"
                elif sell_price < lead_price: order_mode = 'spot_isolated'
            
            # 如果价值低于买入价值，则买入指定数量的币种
            if sell_price > 0 and sell_value <= values["buy_value"]:
                if order_mode == "spot_isolated" and buy_price / sell_price <= 0.98:
                    print(f"买卖价差: {round(buy_price/sell_price,2)} <= 0.98 暂不买入！")
                    continue
                if order_mode != 'spot_isolated' and values["st"] != 0: continue
                quantity = values['trade_amount']
                if usdt_balance < quantity: continue
                # 带单模式、简单交易模式限价单（tdMode参数值根据配置的到）
                if order_mode == 'spot_isolated': spot_isolated_times = spot_isolated_times + 1
                result = okxApi.trade.set_order(symbol, order_mode, "buy", "market", quantity)
                if result and result['code'] == '0':
                    print(f"买入 {coin} {order_mode}，数量为 {quantity}，成交价为 {sell_price} USDT")
                else:
                    if order_mode == "spot_isolated":
                        result = okxApi.trade.set_order(symbol, "cash", "buy", "market", quantity)
                    if result and result['code'] == '0':
                        print(f"买入 {coin} cash，数量为 {quantity}，成交价为 {sell_price} USDT")
                    else:
                        print(f'买入 {order_mode} {quantity} 失败:', result)
                if result and result['code'] == '0':
                    if virtual_balance > 0: virtual_balance -= values['trade_amount'] / buy_price / 10
                    usdt_balance -= quantity
                else: err_coin += coin + " "
            # 如果价值高于卖出价值，则卖出指定数量的币种
            elif buy_value >= values['sell_value']:
                if success != False:
                    sleep_time = 10
                    while success != False:
                        if buy_price > min_buy_price * 1.3: time.sleep(1)
                        elif buy_price > min_buy_price * 1.2: time.sleep(2)
                        elif buy_price > min_buy_price * 1.1: time.sleep(5)
                        elif buy_price > min_buy_price * 1.05: time.sleep(11)
                        else: time.sleep(15)
                        result = okxApiSub.market_get_ticker(symbol)
                        if result and result["code"] == "0": buy_price = float(result['data'][0]['bidPx'])
                        success, min_buy_price, max_buy_price = close_most_profitable_order(success, symbol, buy_price, profit_rate)
                else:
                    # 计算卖出金额及数量 
                    trade_amount = buy_value - values['sell_value'] + values['trade_amount']
                    if sell_price < min_buy_price * 0.94: trade_amount += values['trade_amount'] * 0.75
                    quantity = round(trade_amount / buy_price, values['quantityScale'])

                    # 判断余额是否够卖
                    if (asset_balance + saving_balance) * buy_price < trade_amount or trade_amount < 5.20: continue

                    # 卖出虚拟余额
                    if virtual_balance > 0 and lead_price > sell_price:
                        virtual_balance = virtual_balance - quantity if virtual_balance >= quantity else 0
                        values["virtual_balance"] = virtual_balance if virtual_balance > 0 else 0
                        print(f"卖出虚拟余额 {coin}，金额为 {trade_amount}，成交价为 {buy_price} USDT")
                        continue

                    # 现货不够卖，则全部卖出
                    if asset_balance + saving_balance - virtual_balance < quantity:
                        quantity = truncate(asset_balance + saving_balance - virtual_balance, values['quantityScale'], 'float')
                        if virtual_balance > 0: virtual_balance -= values['trade_amount'] / buy_price
                    elif virtual_balance * buy_price + values["trade_amount"] > values['sell_value']:
                        if virtual_balance > 0: virtual_balance -= values['trade_amount'] / buy_price
                    elif virtual_balance > 0: virtual_balance -= values["trade_amount"] / buy_price / 2
                    
                    # 如果有活期理财宝余额，则先赎回活期理财宝到现货
                    if saving_balance > 0:
                        saving_scale = len(str(saving_balance).split(".")[1]) if "." in str(saving_balance) else 0
                        redeem_quantity = min(round(quantity, saving_scale), saving_balance)
                        if redeem_quantity == 0: redeem_quantity = saving_balance
                        result = savings_purchase_redemption(coin, round(redeem_quantity, saving_scale))
                        if result and result['code'] == '0': print(f"赎回 {coin} 数量 {quantity} 成功: {result['msg']}")
                        else: print(f"赎回 {coin} 数量 {quantity} 金额 {trade_amount} 失败: {result}")
                        time.sleep(5)

                    # 带单模式、简单交易模式限价单（tdMode参数值根据配置的到）
                    order_mode = "cash"
                    result = okxApi.trade.set_order(symbol, order_mode, "sell", "market", quantity)
                    if result and result['code'] == '0':
                        print(f"卖出 {coin} {order_mode}，数量为 {quantity}，成交价为 {buy_price} USDT")
                    else:
                        # 带单模式、简单交易模式限价单（tdMode参数值根据配置的到）
                        result = okxApi.trade.set_order(symbol, order_mode, "sell", "market", int(trade_amount))
                        if result and result['code'] == '0':
                            print(f"卖出 {coin} {order_mode}，金额为 {trade_amount}，成交价为 {buy_price} USDT")
                        else:
                            print(f'卖出 {order_mode} 数量 {quantity} 金额 {trade_amount} 失败:', result['msg'])
                            err_coin += coin + " "
            elif asset_balance * buy_price > 0.5 and saving_balance > 0:
                result = okxApiSub.fundingAccount_set_transfer(coin, asset_balance, "18", "6")
                if result and result["code"] == "0":
                    result = okxApi.savings.set_purchase_redempt(coin, asset_balance, "purchase", '0.01')
                    print(f"{coin} 申购: {asset_balance} + {saving_balance}", result)
            values["virtual_balance"] = virtual_balance if virtual_balance > 0 else 0
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S"), symbol, f"Exception:", str(e))
        time.sleep(0.05)
    
    print(time.strftime("%Y-%m-%d %H:%M:%S"), f"sum_buy_value", round(sum_buy_value), "sum_spot_value", round(sum_spot_value), "usdt", round(usdt_balance + usdt_flexible))
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "sold_coin", sold_coin, "err_coin", err_coin, "over_coin", over_coin, "zero_coin", zero_coin)
    
    # 休息时间
    time.sleep(sleep_time)