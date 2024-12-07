import os, time, redis, traceback, random
from chinese_calendar import is_workday
from datetime import datetime, time as time1

import easytrader, easyquotation
from easytrader import grid_strategies
from easytrader.utils.stock import get_today_ipo_data

# 行情来源：新浪 ['sina'] 腾讯 ['tencent', 'qq']
quotation = easyquotation.use('sina')
xiadan_amount_min = 100 # 动态下单金额下界：100元：每单最少买卖100元
xiadan_amount_max = 300 # 动态下单金额上界：300元：每单最少买卖300元
keep_quantity = 800     # 每股最少持仓数量：800股
keep_amount = 2800      # 每股最少持仓金额：2800元
keep_cash = 200         # 现金最少可用余额：200元

# 同花顺 xiadan.exe 路径
xiadan_path = 'C:\\THS\\xiadan.exe'
os.system("taskkill /IM xiadan.exe > NUL 2> NUL")

# redis 连接参数配置
redis_host = 'localhost'
redis_port = 6379
redis_pass = ""

# 持仓参数配置
symbols = {
    # '159509': { 'name': '纳指科技ETF', 'disabled': 1 },
    # '159687': { 'name': '亚太精选ETF', 'disabled': 1 },
    '002456': { 'name': '欧菲光', 'sell_rate': 1.033, 'buy_rate': 0.966 },
}
# print(symbols['002456']['sell_rate'])

# 截断小数，不四舍五入
def truncate(number, decimal_places, return_type="string"):
    factor = 10 ** decimal_places
    truncated_number = int(number * factor) / factor
    if truncated_number == int(truncated_number): truncated_number = int(truncated_number)
    if return_type != "string": return truncated_number
    return f'{truncated_number:.{decimal_places}f}'.rstrip('0').rstrip('.')

# 判断所给日期是否为交易日
def isTradeDay(date = datetime.now()):
    if is_workday(date):
        if datetime.isoweekday(date) < 6:
            return True
    return False

# 判断所给时间是否为交易时间
def isTradingTime(now = datetime.now()):
    now_time = now.time()
    return (time1(9,15,0) <= now_time < time1(11,35,0)) or (time1(12,58,30) <= now_time < time1(14,58,0))

# 控制台输出当前时间及信息
def print_time(*messages):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(current_time, *messages)

# 连接Redis...
print_time("连接Redis...")
pool = redis.ConnectionPool(host=redis_host,port=redis_port,password=redis_pass,db=0,decode_responses=True)
r = redis.Redis(connection_pool=pool)

user = None; cnt = 0
while True:
    try:
        # 是否交易日，是否交易时间
        now = datetime.now(); buy_count = sell_count = 0
        # now = datetime.strptime("2024-06-10 10:00:00", "%Y-%m-%d %H:%M:%S")
        is_trade_day = isTradeDay(now)
        is_trade_time = isTradingTime(now)
        if not is_trade_day or not is_trade_time:
            is_trade_time_815 = time1(8,15,0) < now.time() < time1(15,0,0)
            sleep_time = 360 if is_trade_day and is_trade_time_815 else 3600
            print_time("是否交易日", is_trade_day, "是否交易时间", is_trade_time, "休息", sleep_time, "秒")
            if not is_trade_time_815 and user != None:
                user.exit(); user = None; cnt = 0
                print_time("退出同花顺...")
            time.sleep(sleep_time)
            continue
        else: sleep_time = 360

        # 启动同花顺：xiadan.exe
        if cnt == 0:
            print_time("启动同花顺", xiadan_path)
            os.system(f'start %s' % xiadan_path)
            time.sleep(60)  # 等待同花顺客户端启动
            user = easytrader.use('ths')
            user.connect(xiadan_path)

        # 默认获取 Grid 数据的策略是通过剪切板拷贝
        user.grid_strategy = grid_strategies.Copy

        # 某些券商客户端无法输入文本
        user.enable_type_keys_for_editor()
        # user.buy("512400", price=truncate(1.0575+0.01,2), amount=100); exit()

        # 9. 查询今日可申购新股
        now = datetime.now()
        # ipo_data = get_today_ipo_data(); now = datetime.now()
        # # print_time("ipo_data", ipo_data)
        # if ipo_data and len(ipo_data) > 0 and time1(9,30,0) <= now.time() <= time1(9,40,0):
        #    # 5. 一键打新
        #    print_time("一键打新", ipo_data)
        #    user.auto_ipo()
        
        # 10. 刷新数据
        # user.refresh()
        
        # 1. 获取资金状况
        # {'资金余额': 13615.92, '可用金额': 13615.92, '可取金额': 0.0, '股票市值': 864671.7, '总资产': 878287.62}
        user_balance = user.balance
        cash_balance = user_balance['可用金额']
        stock_balance = user_balance['股票市值']
        print_time(f"可用金额: {cash_balance}, 股票市值: {stock_balance}")

        # 2. 获取持仓
        # [{'明细': '', '序号': 1, '证券代码': '000413', '证券名称': '东旭光电', 
        # '股票余额': 3800, '实际数量': 3800, '可用余额': 3800, '冻结数量': 0, 
        # '成本价': 1.422, '市价': 1.43, '盈亏': 30.24, '盈亏比(%)': 0.56, 
        # '市值': 5434.0, '当日买入': 0, '当日卖出': 0, '交易市场': '深Ａ', 
        # 'checksum1': 'n23cBDOET5', 'checksum2': 'HwYhvx8W46V3', 'Unnamed: 18': ''}]
        positions = user.position; onhand_balance = 0
        if positions and len(positions) > 0:
            xiadan_amount = xiadan_amount_min # 动态下单金额
            if cash_balance > len(positions) * xiadan_amount_min:
                if now.time() < time1(9,17,0): cash_balance = cash_balance / 2
                xiadan_amount = min(xiadan_amount_max, int(cash_balance / len(positions) / 100) * 100)
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"持仓数量: {len(positions)}，动态下单金额: {xiadan_amount} 元")
            random.shuffle(positions) # 乱序遍历持仓
            for position in positions:
                try:
                    asset_value = position["市值"]
                    onhand_balance += asset_value
                    now = datetime.now(); is_trade_day = isTradeDay(now)
                    if not is_trade_day or now.time() < time1(9,15,0) or now.time() >= time1(14,59,50): continue
                    asset_order = position["序号"]
                    asset_code = position["证券代码"]
                    if asset_code in symbols and "disabled" in symbols[asset_code]: r.hdel("THS:price", asset_code); continue
                    asset_name = position["证券名称"]
                    asset_balance = position["实际数量"]
                    if asset_balance < 100: continue
                    asset_available = position["可用余额"]
                    asset_cost_price = position["成本价"]
                    asset_market_price = position["市价"]
                    asset_profit = position["盈亏"]
                    asset_today_buy = position["当日买入"]
                    asset_today_sell = position["当日卖出"]
                    last_price = r.hget("THS:price", asset_code)
                    if last_price == None or float(last_price) < 0.1:
                        last_price = asset_market_price
                        r.hset("THS:price", asset_code, asset_market_price)
                        print(asset_order, asset_code, asset_name, asset_balance, asset_market_price, asset_value)
                    sell_rate = 1.0051; buy_rate = 0.9949
                    if "ETF" in asset_name:
                        if asset_market_price > 5: sell_rate = 1.0151; buy_rate = 0.9849
                        elif asset_market_price > 4: sell_rate = 1.0131; buy_rate = 0.9869
                        elif asset_market_price > 3: sell_rate = 1.0101; buy_rate = 0.9899
                        elif asset_market_price > 2: sell_rate = 1.0071; buy_rate = 0.9929
                    elif asset_market_price > 5: sell_rate = 1.0331; buy_rate = 0.9669
                    elif asset_market_price > 3: sell_rate = 1.0249; buy_rate = 0.9751
                    elif asset_market_price > 2: sell_rate = 1.0151; buy_rate = 0.9849
                    elif asset_market_price > 1: sell_rate = 1.0111; buy_rate = 0.9889
                    elif asset_market_price <= 0: continue
                    if asset_code in symbols:
                        if "buy_rate" in symbols[asset_code]: buy_rate = float(symbols[asset_code]["buy_rate"])
                        if "sell_rate" in symbols[asset_code]: sell_rate = float(symbols[asset_code]["sell_rate"])
                    sell_price = round(float(last_price) * sell_rate, 3)
                    buy_price = round(float(last_price) * buy_rate, 3)
                    amount = (int(xiadan_amount / 100 / asset_market_price) + 1) * 100 # 使用【动态下单金额】计算：买入/卖出股数
                    bid_price = asset_market_price; ask_price = asset_market_price
                    data = quotation.real(asset_code)
                    if data and data[asset_code]:
                        bid1 = float(data[asset_code]["bid1"]) # 买一
                        ask1 = float(data[asset_code]["ask1"]) # 卖一
                        if bid1 > 0: bid_price = bid1
                        if ask1 > 0: ask_price = ask1
                    now = datetime.now()
                    if bid_price > sell_price: # 卖出
                        while amount > 100 and asset_available < amount: amount -= 100
                        while amount > 100 and asset_balance - amount < keep_quantity: amount -= 100
                        print_time(asset_order, "卖出", asset_code, asset_name, bid_price, last_price, "->", sell_price, amount, round(cash_balance,2))
                        # 实际数量 > 最小持仓数量 and 可用余额 > 下单数量 and 市值 > 最小持仓金额
                        if asset_balance - amount >= keep_quantity and asset_available >= amount and asset_value > keep_amount:
                            if now.time() >= time1(9,30,0): cash_balance += bid_price * amount; onhand_balance -= bid_price * amount
                            user.sell(asset_code, price=bid_price, amount=amount) # 限价卖出
                            r.hset("THS:price", asset_code, sell_price); sell_count += 1 # time.sleep(0.2); # user.refresh();
                        else:
                            print("持仓不足", asset_code, asset_name, asset_balance, asset_available, asset_value)
                            r.hset("THS:price", asset_code, bid_price)
                    elif ask_price < buy_price: # 买入
                        cash_balance = user.balance['可用金额']
                        print_time(asset_order, "买入", asset_code, asset_name, ask_price, last_price, "->", buy_price, amount, round(cash_balance,2))
                        if cash_balance - keep_cash > ask_price * amount: # 可用金额 - 保持余额 > 买入金额
                            cash_balance -= ask_price * amount; onhand_balance += ask_price * amount
                            user.buy(asset_code, price=ask_price, amount=amount) # 限价买入
                            r.hset("THS:price", asset_code, buy_price); buy_count += 1 # time.sleep(0.2); # user.refresh();
                        else: print("余额不足，请入金，当前余额：", round(cash_balance,2))
                except Exception as e1:
                    # traceback.print_exc()
                    print_time(e1)
        # 持仓余额
        if onhand_balance > 0:
            print_time("持仓余额", round(onhand_balance,3), "可用余额", round(cash_balance,2))

        # 10. 刷新数据
        # time.sleep(5); user.refresh(); time.sleep(5)

    except Exception as e:
        traceback.print_exc(); cnt = 3; sleep_time = 60
    
    cnt += 1
    if cnt >= 3 and user != None:
        # 五、退出客户端软件
        user.exit(); user = None; cnt = 0
        print_time("退出同花顺...")

    # 休息时间
    if buy_count + sell_count >= 10: sleep_time = 60
    time.sleep(sleep_time)
