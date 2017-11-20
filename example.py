# -*- coding: utf-8 -*-

import telegram
from bittrex import bittrex
from poloniex import poloniex
import config

# 변수선언
marketcurrency = 'BTC'  # 기준코인
altcurrency = 'DGB'  # 알트코인
spread = 0.8  # 차이 1% => 1
market_bitt = '{0}-{1}'.format(marketcurrency, altcurrency)
market_polo = '{0}_{1}'.format(marketcurrency, altcurrency)
is_marketcurrency_transfering = False
is_altcurrency_transfering = False
bittrex_api = config.bittrex_api
bittrex_key = config.bittrex_key
poloniex_api = config.poloniex_api
poloniex_key = config.poloniex_key
bitt_marketcurrency_bal = 0
polo_marketcurrency_bal = 0
bitt_altcurrency_bal = 0
polo_altcurrency_bal = 0
bitt_marketcurrency_address = '1DAFcmkeQiMWdhAmwKBLmx9pUpM4yak4DC'
polo_marketcurrency_address = '1J4LrydHhH356J1ykvbXVDsj4a2s2497PP'
bitt_altcurrency_address = 'DPCgJ15dvMSTVvSKUX1LU1s4RZs5Dk2T8H'
polo_altcurrency_address = 'DBCLd1NZpKFjc8eo2RgyWL43a6zBkCqTLP'
telegram_token = config.telegram_token
telegram_chat_id = config.telegram_chat_id

bot = telegram.Bot(token=telegram_token)
# API 객채생성
bitt = bittrex(bittrex_api, bittrex_key)
polo = poloniex(poloniex_api, poloniex_key)

# 출금내역 조회
# [{'PaymentUuid': 'e8e9d626-667f-4aa6-8318-fb8bbf706f34',
# 'Currency': 'BTC',
# 'Amount': 0.01492305,
# 'Address': '1J4LrydHhH356J1ykvbXVDsj4a2s2497PP',
# 'Opened': '2017-11-19T01:35:30.757',
# 'Authorized': True,
# 'PendingPayment': False,
# 'TxCost': 0.001,
# 'TxId': '9b475b99c123a3959d9ce005767d8fb8ba8a54c8057f7ae88269b56ddb02e6a2',
# 'Canceled': False,
# 'InvalidAddress': False}]
print('bittrex 출금내역', bitt.getwithdrawalhistory('BTC', 1))
print('bittrex 입금내역', bitt.getdeposithistory('BTC', 2))

#print('poloniex 입금내역', polo..getdeposithistory('BTC', 2))