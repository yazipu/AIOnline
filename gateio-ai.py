# -*- coding: utf-8 -*-
# https://www.gate.io/docs/developers/apiv4/zh_CN/
api_key = ""
api_secret = ""

virtual_balance_enable = False # 是否启用虚拟余额
usdt_keep = 100     # 保持现货 USDT 余额
keep_step = 50      # 每次赎回 USDT 金额
gt_keep = 10        # 保持现货 GT 余额

# 设置要检测的币种和相应的价值判断
symbols = {
    'GT_USDT': { 'buy_value': 590, 'trade_amount': 12,'earn':20,'kv':200,'st':0 },

    'JASMY_USDT': { 'buy_value': 395, 'trade_amount': 11 },
    'EZSWAP_USDT': { 'buy_value': 390, 'trade_amount': 11 },
    'ORDS_USDT': { 'buy_value': 390, 'trade_amount': 11 },
    'RON_USDT': { 'buy_value': 390, 'trade_amount': 11,'vb':0,'st':0 },

    'AIX_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'BRISE_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'CYCON_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'DOME_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'DOGE2_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'DGI_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'FREE_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'GEC_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'GMRX_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'GOAT_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'LUFFY_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'OX_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'PACK_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'SUDO_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'TENET_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'WAGMIGAMES_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'WOJAK_USDT': { 'buy_value': 290, 'trade_amount': 11 },

    'TRX_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'BTT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'JST_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SUN_USDT': { 'buy_value': 190, 'trade_amount': 11 },

    'RING_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'YFII_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'RLY_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'MNT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'OMG_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'WAVES_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'WNXM_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'XEM_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'GRV_USDT': { 'buy_value': 190, 'trade_amount': 11 },

    'DREP_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'THALES_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'AIBB_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'TROSS_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'TIP_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'CULT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'KIN_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'ALITA_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'MAGA_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'FIGHT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'ZKF_USDT': { 'buy_value': 190, 'trade_amount': 11 },

    'POLC_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'UFO_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'STARL_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'HAM_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'ABBC_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'STRM_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'CHATAI_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'QUACK_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SOLS_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'ADF_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'WLKN_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'MCRT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'VINU_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'CEUR_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'CAL_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'TYPE_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'POGAI_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'ZERO_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'IQ50_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SNAP_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'HAMSTER_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'GMMT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'KAT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'OVR_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'POKT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'CAF_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'OPTIMUS_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'MOVEZ_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'PUMP_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SYNC_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'X_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'CROS_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'DINO_USDT': { 'buy_value': 190, 'trade_amount': 11 },

    'NEVER_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SAKAI_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'PBUX_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'WATERSOL_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'CSIX_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    '3ULL_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'AVA_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'DZOO_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'LIME_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'LOVELY_USDT': { 'buy_value': 190, 'trade_amount': 11 },

    'SMOLE_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'INSP_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'PLANET_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'RFD_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SKEB_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'KAIA_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'AWT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'PEPEBRC_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    
    'GRASS_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'FUSE_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'AMU_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'PUMLX_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'PPAD_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'LM_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'BRCT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'GQ_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'BOMB_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'TURT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SHILL_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'CITY_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'IGU_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'BD20_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'VOLT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'BAN_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'GLM_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'AD_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'BBL_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'COM_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'PNUT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SNEK_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'DEFI_USDT': { 'buy_value': 190, 'trade_amount': 11 },

    'ACT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'DOGE_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'PEPE_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'HBAR_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'ALGO_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'KAS_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'ENS_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'PUFFER_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'VIRTUAL_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'CORE_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'WLD_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'TON_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'XRP_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'ADA_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'XLM_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'FET_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SOL_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'APP_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'ONDO_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SUI_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    
    'AIMX_USDT': { 'buy_value': 290, 'trade_amount': 11 },
    'KOK_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'OM_USDT': { 'buy_value': 190, 'trade_amount': 11 },

    'MOODENG_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'LINK_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'DOT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'CRV_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'ORDI_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'EOS_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'TAO_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'LTC_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SHIB_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'ENA_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'AVAX_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SEI_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'RATS_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'FTM_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'CFX_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'FIL_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'XMR_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'NEAR_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'UNI_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'TIA_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'APT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'BNB_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'JUP_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'WIF_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'MOG_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'BOME_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'XVG_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SAND_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'TURBO_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'NERD_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'NEXG_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'SAFE_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'JOY_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'QNT_USDT': { 'buy_value': 190, 'trade_amount': 11 },
    'ORCA_USDT': { 'buy_value': 190, 'trade_amount': 11 },

    # 下架/清仓
    # 'NADA_USDT': { 'buy_value': 190, 'trade_amount': 11,'st':4 },

}

import requests, json, hashlib, hmac, time, base64

class GateioAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.gateio.ws"
        self.prefix = "/api/v4"
        self.common_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def _generate_signature(self, method, endpoint, query_string=None, payload_string=None):
        t = int(time.time())
        hashed_payload = hashlib.sha512((payload_string or '').encode('utf-8')).hexdigest()
        signature_data = f'{method}\n{self.prefix}{endpoint}\n{query_string or ""}\n{hashed_payload}\n{t}'
        # print("signature_data", signature_data, payload_string)
        sign = hmac.new(self.api_secret.encode('utf-8'), signature_data.encode('utf-8'), hashlib.sha512).hexdigest()
        return {'KEY': self.api_key, 'Timestamp': str(t), 'SIGN': sign}

    def _send_request(self, method, endpoint, query_string=None, data=None):
        try:
            url = f"{self.base_url}{self.prefix}{endpoint}"
            payload_string = json.dumps(data) if method.lower() == 'post' else None
            sign_headers = self._generate_signature(method, endpoint, query_string, payload_string)
            sign_headers.update(self.common_headers)
            # print('signature headers: %s' % sign_headers)
            response = requests.request(method, url, params=query_string, data=payload_string, headers=sign_headers, timeout=30)
            # print(response.content)
            # response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            if response.status_code == 200: return response.json()
            return response.content
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"Exception:", str(e))
        return None

    def get_spot_balance(self): return self._send_request('GET', '/spot/accounts')
    def get_spot_currencies(self): return self._send_request('GET', '/spot/currencies')
    def get_spot_currency_pairs(self): return self._send_request('GET', '/spot/currency_pairs')
    def get_spot_tickers(self): return self._send_request('GET', '/spot/tickers')
    def get_earn_uni_lends(self, page = 1, limit = 100):
        query_param = f"page={page}&limit={limit}"
        return self._send_request('GET', '/earn/uni/lends', query_param)
    def post_earn_uni_lends(self, _currency, _amount, _type, _min_rate = 0):
        data = { 'currency': _currency, 'amount': _amount, 'type': _type, 'min_rate': _min_rate }
        return self._send_request('POST', '/earn/uni/lends', None, data)
    def post_spot_batch_orders(self, data): return self._send_request('POST', '/spot/batch_orders', None, data)
    def post_spot_orders(self, _currency_pair, _side, _type, _amount, _time_in_force = 'fok'):
        data = {
            'currency_pair': _currency_pair,
            'side': _side,
            'type': _type,
            'amount': _amount,
            'time_in_force': _time_in_force
        }
        return self._send_request('POST', '/spot/orders', None, data)

# 截断小数，不四舍五入
def truncate(number, decimal_places, return_type="string"):
    factor = 10 ** decimal_places
    truncated_number = int(number * factor) / factor
    if truncated_number == int(truncated_number): truncated_number = int(truncated_number)
    if return_type != "string": return truncated_number
    return f'{truncated_number:.{decimal_places}f}'.rstrip('0').rstrip('.')

# Create GateioAPI instance
gateio_api = GateioAPI(api_key, api_secret)

# 获取现货交易对精度
spot_currency_pairs = gateio_api.get_spot_currency_pairs()
if spot_currency_pairs != None:
    for symbol, values in symbols.items():
        values["price_scale"] = values["num_dp"] if "num_dp" in values else 0
        values["quantity_scale"] = values["num_dp"] if "num_dp" in values else 0
        for spot_symbol in spot_currency_pairs:
            if symbol == spot_symbol["id"]:
                # print("spot_symbol", spot_symbol)
                values["price_scale"] = int(spot_symbol["precision"])
                values["quantity_scale"] = int(spot_symbol["amount_precision"])
# print("symbols", symbols)

# 每10分钟执行一次检测和交易操作
savings_product = {}
while True:
    try:
        i = 0
        quantity = 0

        # 查询GT活期余币宝信息
        spot_trader_enable = False
        spot_trace_symbol_list = []
        
        # 查询活期余币宝资产信息
        retry = 0
        min_id = ""
        savings_list = []
        for page in range(1, 1000):
            result = gateio_api.get_earn_uni_lends(page=page,limit=100)
            if result != None:
                savings_list.extend(result)
                if len(result) < 100: break
                else: time.sleep(0.1)
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S"), f"获取【活期理财宝】资产失败: {result}")
                retry = retry + 1
                if retry > 60: exit()
                else: time.sleep(10)
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "当前【活期余币宝】资产数量", len(savings_list))
        
        # 获取账户余额
        balances = gateio_api.get_spot_balance()
        
        # 检查USDT现货余额，保持50+
        usdt_balance = 0
        usdt_flexible = 0
        # USDT 现货余额
        for balance in balances:
            if balance['currency'] == "USDT":
                usdt_balance = round(float(balance['available']), 6)
            elif float(balance['available']) > 0:
                exist = False
                for symbol, values in symbols.items():
                    if balance['currency'] == symbol[:-5]:
                        exist = True
                        break
                if exist == False: print(balance['currency'], "余额", round(float(balance['available']), 2), "未配置！")
        # USDT 活期理财余额
        for saving in savings_list:
            if saving['currency'] == "USDT":
                usdt_flexible = round(float(saving['amount']), 6)
                break
        print(f"USDT:{usdt_balance} 活期:{usdt_flexible}")

        if usdt_balance < usdt_keep and usdt_flexible >= keep_step:
            result = gateio_api.post_earn_uni_lends("USDT", keep_step, "redeem")
            print(f"赎回 {keep_step} USDT : {result}")
            # time.sleep(5)
        elif usdt_balance > usdt_keep * 3:
            lend_usdt = int(usdt_balance - usdt_keep * 2)
            result = gateio_api.post_earn_uni_lends("USDT", lend_usdt, "lend", 0.0001)
            print(f"申购 {lend_usdt} USDT : {result}")
        
        # 检查GT现货余额，用于支付交易手续费
        gt_balance = 0
        gt_flexible = 0
        # GT 现货余额
        for balance in balances:
            if balance['currency'] == "GT":
                gt_balance = round(float(balance['available']), 2)
                break
        # GT 活期理财余额
        for saving in savings_list:
            if saving['currency'] == "GT":
                gt_flexible = round(float(saving['amount']), 2)
                break
        if gt_balance < gt_keep and gt_flexible >= gt_keep:
            result = gateio_api.post_earn_uni_lends("GT", gt_keep, "redeem")
            print(f"赎回 {gt_keep} GT: {result}")
        print(f"GT:{gt_balance} 活期:{gt_flexible}")
        
        # 获取全部行情信息
        ticker_time = int(time.time() * 1000) + 1500
        ticker_list = gateio_api.get_spot_tickers()
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"行情数量: {len(ticker_list)}  时间戳: {ticker_time}")
        if len(ticker_list) < 100: continue
        
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "Exception:", str(e))
        time.sleep(30)
        continue

    sleep_time = 60; sum_buy_value = 0; sum_spot_value = 0; sold_coin = err_coin = zero_coin = ""; order_time = time.time()
    for symbol, values in symbols.items():
        try:
            i = i + 1
            coin = symbol[:-5]
            asset_balance = 0; saving_balance = 0
            for balance in balances:
                if balance['currency'] == coin:
                    asset_balance = float(balance['available'])
                    if asset_balance == int(asset_balance): asset_balance = int(asset_balance)
                    break
            for saving in savings_list:
                if saving['currency'] == coin:
                    saving_balance = float(saving['amount'])
                    if saving_balance == int(saving_balance): saving_balance = int(saving_balance)
                    break
            symbol_balance = asset_balance + saving_balance
            # print("asset_balance", asset_balance, "saving_balance", saving_balance)

            # 获取当前币种价格
            buy_price = 0; sell_price = 0
            if ticker_time < int(time.time() * 1000):
                ticker_list = gateio_api.get_spot_tickers()
                if len(ticker_list) < 100: continue
                ticker_time = int(time.time() * 1000) + 1500
            for ticker in ticker_list:
                if symbol == ticker["currency_pair"]:
                    buy_price = float(ticker['highest_bid'])
                    sell_price = float(ticker['lowest_ask'])
                    break
            # print("price", buy_price, sell_price)

            # 虚拟余额
            if buy_price <= 0 or sell_price <= 0: print(f"{i}. {coin} 获取价格失败!!!"); err_coin += coin + " "; continue
            if int(symbol_balance * buy_price) <= 5: zero_coin += coin + " "
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
            buy_value = round(symbol_balance * buy_price, values["price_scale"])
            sell_value = round(symbol_balance * sell_price, values["price_scale"])
            sum_buy_value += buy_value; sum_spot_value += buy_value - virtual_buy_value
            
            if not "st" in values: values["st"] = 0 # 0-正常持币，4-立刻清仓
                
            # 带单计算：trade_amount
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
                bid_value = round(values["buy_value"] * (1.028 - buy_price / sell_price))
                values["sell_value"] = max(values["buy_value"] + max(20, bid_value * 2), values["sell_value"] if "sell_value" in values else 0)
                if bid_rate >= 1.5:
                    print(f"{coin} 价差：{bid_rate}% {bid_value}", "buy_value", values["buy_value"], "sell_value", values["sell_value"], "trade_amount", values["trade_amount"])
            elif not "sell_value" in values or values["sell_value"] < values["buy_value"] + 10:
                if values["trade_amount"] < 10: values["sell_value"] = values["buy_value"] + 12
                else: values["sell_value"] = round(values["buy_value"] + values["trade_amount"] * 1.98, 0)
                # print(values)
            
            print(time.strftime("%Y-%m-%d %H:%M:%S"), f"{i}. {coin}  价格:{truncate(sell_price,10)}  余额 buy:{int(buy_value-virtual_buy_value)}{'+'+str(int(virtual_buy_value)) if virtual_balance>0 else''} sell:{int(sell_value)} st:{values['st']}"),  # 数量小数位数：{precision}
            
            # 如果价值低于买入价值，则买入指定数量的币种
            if sell_price > 0 and sell_value < values['buy_value']:
                quantity = values['trade_amount']
                if usdt_balance < quantity: continue
                # 买入现货
                response = gateio_api.post_spot_orders(symbol, 'buy', 'market', quantity)
                print(f"买入 {coin}，数量为 {quantity}，成交价为 {sell_price} USDT", response)
                if virtual_balance > 0: virtual_balance -= values['trade_amount'] / buy_price / 10
            # 如果价值高于卖出价值，则卖出指定数量的币种
            elif buy_value >= values['sell_value']:
                # 计算卖出金额及数量
                trade_amount = buy_value - values['sell_value'] + values['trade_amount']
                # if sell_price < min_buy_price * 0.94: trade_amount += values['trade_amount'] * 0.75
                quantity = round(trade_amount / buy_price, values['quantity_scale'])
                # 判断余额是否够卖
                if symbol_balance * buy_price < trade_amount or trade_amount < 5.20: continue
                print(f'{symbol} bv: {values["buy_value"]}, sv: {values["sell_value"]}, ta: {trade_amount}')

                # 卖出虚拟余额
                if virtual_balance > 0 and lead_price > sell_price: # and symbol_balance - virtual_balance < quantity:
                    virtual_balance = virtual_balance - quantity if virtual_balance >= quantity else 0
                    values["virtual_balance"] = virtual_balance if virtual_balance > 0 else 0
                    print(f"卖出虚拟余额 {coin}，金额为 {trade_amount}，成交价为 {buy_price} USDT")
                    continue

                # 现货不够卖，则全部卖出
                if symbol_balance - virtual_balance < quantity:
                    quantity = truncate(symbol_balance - virtual_balance, values['quantity_scale'], 'float')
                    if virtual_balance > 0: virtual_balance -= values['trade_amount'] / buy_price
                elif virtual_balance * buy_price + values["trade_amount"] > values['sell_value']:
                    if virtual_balance > 0: virtual_balance -= values['trade_amount'] / buy_price
                elif virtual_balance > 0: virtual_balance -= values["trade_amount"] / buy_price / 2

                # 如果有活期余币宝余额，则先赎回活期余币宝到现货
                redeem_quantity = 0
                if saving_balance > 0: # asset_balance < quantity and
                    saving_scale = len(str(saving_balance).split(".")[1]) if "." in str(saving_balance) else 0
                    redeem_quantity = min(round(quantity, saving_scale), saving_balance)
                    if redeem_quantity == 0: redeem_quantity = saving_balance
                    result = gateio_api.post_earn_uni_lends(coin, redeem_quantity, "redeem")
                    print(f"赎回 {coin} 数量 {redeem_quantity}: {result}")
                    time.sleep(5)
                # 卖出现货
                response = gateio_api.post_spot_orders(symbol, 'sell', 'market', quantity)
                print(f'卖出 {coin}，数量 {quantity} 金额 {trade_amount}:', response); sold_coin += coin + " "
            values["virtual_balance"] = virtual_balance if virtual_balance > 0 else 0
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S"), symbol, f"Exception:", str(e))
        
        time.sleep(0.05)
    
    print(time.strftime("%Y-%m-%d %H:%M:%S"), f"sum_buy_value", round(sum_buy_value), "sum_spot_value", round(sum_spot_value), "usdt", round(usdt_balance + usdt_flexible))
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "sold_coin", sold_coin, "err_coin", err_coin, "zero_coin", zero_coin)

    # 休息时间
    time.sleep(sleep_time)
