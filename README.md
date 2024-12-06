# AIOnline - 爱神交易策略创始人

## 原理：
    低卖高卖，始终保持【固定金额】仓位。
    
## 美股：
    pip install ibkr.cmd                安装 IBKR 所需类库
    python ibkr-ai.py                   IBKR 盈透证券

## A股：
    pip install easytrader.cmd          安装 EasyTrader 所需类库
    python ths.py                       同花顺 + 银河证券

## 币币：
    pip install coin.cmd                安装币币所需类库

####  已完成:
    python binance-ai.py               Binance 币安交易所（现货+现货带单）
    python bitget-ai.py                BitGet 交易所（现货+现贷带单）
    python gateio-ai.py                GateIO 狗头交易所（现货）
    python okx-ai.py                   OKX 欧易交易所（现货+现货带单）
  
####  未完成:
    python bybit-ai.py                 Bybit 交易所（现货）
    python htx-ai.py                   HTX 火币交易所（现货）
    python mexc-ai.py                  MEXC 抹茶交易所（现货）
    
## 爱神交易策略【手工交易】举例：
####    基础：【固定金额持仓】
    1、选择优质资产：如【沪深300】、【标普500】、【道琼斯】、【纳斯达克】、【黄金】、【石油】、【BTC】等
    2、【建仓金额】举例： 10,000 元
    3、持仓金额【涨到】 10,500 元，则【卖出】：500 元
    4、持仓金额【跌到】  9,500 元，则【买入】：500 元
    
####    进阶：【加仓】/【减仓】
    5、每跌【20%至30%】以上，【DCA 加仓】： 11000 -> 12000 -> 15000 -> 20000 ...
    6、每涨【20%至30%】以上，【DCA 减仓】： 9000 -> 8000 -> 7000 -> 5000 ...
    
## 观点：
    用有限的资金，赚无限的梦想
    
    用【DCA 定投】策略【建仓】
    用【马丁格尔】策略【加仓】
    用【网格交易】策略【降本】
    用【爱神交易】策略【守仓】
    
    坚持投资，积累财富，持续盈利，扭转人生！
    小跌小买，中跌中买，大跌大买，极跌极买，
    小涨小卖，中跌中卖，大跌大卖，极跌极卖！
    DCA囤现货，持币待涨，迎接大牛！
