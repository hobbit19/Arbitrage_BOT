# -*- coding: utf-8 -*-

import telegram

import config
from exchage_api.bittrex import bittrex
from exchage_api.poloniex import poloniex

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

# Market Currency 잔고 조회
try:
    bitt_marketcurrency_bal = float(bitt.getbalance(marketcurrency)['Available'])
except:
    print('bittrex get balance error-{0}'.format(bitt.getbalance(marketcurrency)['Available']))
    bitt_marketcurrency_bal = 0
try:
    polo_marketcurrency_bal = float(polo.returnBalances()[marketcurrency])
except:
    print('poloniex get balance error-{0}'.format(polo.returnBalances()[marketcurrency]))
    polo_marketcurrency_bal = 0
total_marketcurrency_bal = bitt_marketcurrency_bal + polo_marketcurrency_bal
print('bittrex : {0:8f}{1} / poloniex : {2:8f}{3}'.format(bitt_marketcurrency_bal, marketcurrency, polo_marketcurrency_bal, marketcurrency))

# Alt Currency 잔고 확인
try:
    bitt_altcurrency_bal = float(bitt.getbalance(altcurrency)['Available'])
except:
    bitt_altcurrency_bal = 0
try:
    polo_altcurrency_bal = float(polo.returnBalances()[altcurrency])
except:
    polo_altcurrency_bal = 0
total_altcurrency_bal = bitt_altcurrency_bal + polo_altcurrency_bal
print('bittrex : {0:8f}{1} / poloniex : {2:8f}{3} '.format(bitt_altcurrency_bal, altcurrency, polo_altcurrency_bal,
                                                           altcurrency))
#print('poloniex 입금내역', polo..getdeposithistory('BTC', 2))