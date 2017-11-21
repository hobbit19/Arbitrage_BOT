# -*- coding: utf-8 -*-

import telegram
from bittrex import bittrex
from poloniex import poloniex
import config

# 변수선언
marketcurrency = config.markgetcurrency  # 기준코인
altcurrency = config.altcurrency # 알트코인
spread = 0.8  # 차이 1% => 1
bitt_market = '{0}-{1}'.format(marketcurrency, altcurrency)
polo_market = '{0}_{1}'.format(marketcurrency, altcurrency)
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


def send_message(msg=None):
    print(msg)
    #bot.sendMessage(chat_id=telegram_chat_id, text=msg)


def send_message_with_error(message=None):
    msg = f"⚠️ Error - wait 10 min\n{0}".format(message)
    print(msg)
    bot.sendMessage(chat_id=telegram_chat_id, text=msg)


# 잔고조정
def balancing():
    global bitt_marketcurrency_bal
    global polo_marketcurrency_bal
    global bitt_altcurrency_bal
    global polo_altcurrency_bal
    global is_marketcurrency_transfering
    global is_altcurrency_transfering

    # 이체 중 인지 판단
    # 송금하면 송금플래그를 true 로변경
    # 송금전의 잔액 기억하고 있다가 송금한 금액만큼(수수료 감안) 증가하면 이체완료로 간주한다

    is_marketcurrency_transfering = False
    if not is_marketcurrency_transfering:
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

        # Market Currency 잔고 조정
        if bitt_marketcurrency_bal / total_marketcurrency_bal > 0.8:
            try:
                transfer_amount = bitt_marketcurrency_bal - (total_marketcurrency_bal / 2)
                #bitt.withdraw(marketcurrency, transfer_amount, polo_marketcurrency_address)
                send_message('withdraw to Poloniex : {0:8f}{1}'.format(transfer_amount, marketcurrency))
            except:
                send_message_with_error('error')
        if polo_marketcurrency_bal / total_marketcurrency_bal > 0.8:
            try:
                transfer_amount = polo_marketcurrency_bal - (total_marketcurrency_bal / 2)
                #polo.withdraw(marketcurrency, transfer_amount, bitt_marketcurrency_address)
                send_message('withdraw to Bittrex : {0:8f}{1}'.format(transfer_amount, marketcurrency))
            except:
                send_message_with_error('error')

    # Alt Currency 잔고 확인
    is_altcurrency_transfering = False
    if not is_altcurrency_transfering:
        try:
            bitt_altcurrency_bal = float(bitt.getbalance(altcurrency)['Available'])
        except:
            bitt_altcurrency_bal = 0
        try:
            polo_altcurrency_bal = float(polo.returnBalances()[altcurrency])
        except:
            polo_altcurrency_bal = 0
        total_altcurrency_bal = bitt_altcurrency_bal + polo_altcurrency_bal
        print('bittrex : {0:8f}{1} / poloniex : {2:8f}{3} '.format(bitt_altcurrency_bal, altcurrency, polo_altcurrency_bal, altcurrency))

    # Alt Currency 잔고 조정
    if bitt_altcurrency_bal / total_altcurrency_bal > 0.8:
        try:
            transfer_amount = bitt_altcurrency_bal - (total_altcurrency_bal / 2)
            #bitt.withdraw(altcurrency, transfer_amount, polo_altcurrency_address)
            send_message('withdraw to Poloniex : {0:8f}{1}'.format(transfer_amount, altcurrency))
        except:
            send_message_with_error('withdraw to Poloniex : {0:8f}{1}'.format(transfer_amount,altcurrency))
    if polo_altcurrency_bal / total_altcurrency_bal > 0.8:
        try:
            transfer_amount = polo_altcurrency_bal - (total_altcurrency_bal / 2)
            #polo.withdraw(altcurrency, transfer_amount, bitt_altcurrency_address)
            send_message('withdraw to Bittrex : {0:8f}{1}'.format(transfer_amount, altcurrency))
        except:
            send_message_with_error('withdraw to Bittrex : {0:8f}{1}'.format(transfer_amount,altcurrency))


# 오더북 조회
def getorderbook():
    # Bittrexx 오더북 조회
    bitt_orderbook = bitt.getorderbook(bitt_market, 'both', 20)
    bitt_buyorder = bitt_orderbook['buy']
    bitt_sellorder = bitt_orderbook['sell']
    polo_orderbook = polo.returnOrderBook(polo_market)
    polo_buyorder = polo_orderbook['bids']
    polo_sellorder = polo_orderbook['asks']
    '''
    for order in bitt_buyorder:
        print(float(order['Rate'])*1000) #내림차순
    print("------------------------------------------")
    for order in polo_buyorder:   #내림차순
        print(order[0])
    '''
    for order in bitt_sellorder:
        print(float(order['Rate'])*1000) #오름차순
    print("------------------------------------------")
    for order in polo_sellorder:   #오름차순
        print(order[0])
##오더

'''
print(polo.returnTicker())
# Getting the BTC price for DGB
currencysummary = bitt.getmarketsummary(market_bitt)
currencyprice = currencysummary[0]['Last']
#print ('The price for {0} is {1:.8f} {2}.'.format(currency, currencyprice, trade))

# 전체 잔고조회
balances = bitt.getbalances()
for coin in balances:
    if coin['Balance'] == 0:
        continue
    print('{0} : {1:.8f}'.format(coin['Currency'], coin['Balance']))

#dogebalance = bittApi.getbalance(currency)
'''

if __name__ == '__main__':
    #balancing()
    getorderbook()
