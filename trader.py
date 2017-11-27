# -*- coding: utf-8 -*-
import telegram
import time
import sys
import config
from exchage_api.bittrex import bittrex
from exchage_api.poloniex import poloniex
import util

# 변수선언
marketcurrency = config.markgetcurrency  # 기준코인
#altcurrency = config.altcurrency # 알트코인
altcurrency = 'DGB' # 알트코인
spread = 0.8  # 차이 0.8%
bittrex_market = '{0}-{1}'.format(marketcurrency, altcurrency)
poloniex_market = '{0}_{1}'.format(marketcurrency, altcurrency)
is_marketcurrency_transfering = False
is_altcurrency_transfering = False
bittrex_api = config.bittrex_api
bittrex_key = config.bittrex_key
poloniex_api = config.poloniex_api
poloniex_key = config.poloniex_key
bittrex_marketcurrency_bal = 0
poloniex_marketcurrency_bal = 0
bittrex_altcurrency_bal = 0
poloniex_altcurrency_bal = 0
bittrex_marketcurrency_address = '1DAFcmkeQiMWdhAmwKBLmx9pUpM4yak4DC'
poloniex_marketcurrency_address = '1J4LrydHhH356J1ykvbXVDsj4a2s2497PP'
bittrex_altcurrency_address = 'DPCgJ15dvMSTVvSKUX1LU1s4RZs5Dk2T8H'
poloniex_altcurrency_address = 'DBCLd1NZpKFjc8eo2RgyWL43a6zBkCqTLP'
telegram_token = config.telegram_token
telegram_chat_id = config.telegram_chat_id
spread = 0.8 # %
spread = spread / 100
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
    global bittrex_marketcurrency_bal
    global poloniex_marketcurrency_bal
    global bittrex_altcurrency_bal
    global poloniex_altcurrency_bal
    global is_marketcurrency_transfering
    global is_altcurrency_transfering

    # 이체 중 인지 판단
    # 송금하면 송금플래그를 true 로변경
    # 송금전의 잔액 기억하고 있다가 송금한 금액만큼(수수료 감안) 증가하면 이체완료로 간주한다

    is_marketcurrency_transfering = False
    if not is_marketcurrency_transfering:
        # Market Currency 잔고 조회
        try:
            bittrex_marketcurrency_bal = float(bitt.getbalance(marketcurrency)['Available'])
        except:
            print('bittrex get balance error-{0}'.format(bitt.getbalance(marketcurrency)['Available']))
            bittrex_marketcurrency_bal = 0
        try:
            poloniex_marketcurrency_bal = float(polo.returnBalances()[marketcurrency])
        except:
            print('poloniex get balance error-{0}'.format(polo.returnBalances()[marketcurrency]))
            poloniex_marketcurrency_bal = 0
        total_marketcurrency_bal = bittrex_marketcurrency_bal + poloniex_marketcurrency_bal
        print('bittrex : {0:8f}{1} / poloniex : {2:8f}{3}'.format(bittrex_marketcurrency_bal, marketcurrency, poloniex_marketcurrency_bal, marketcurrency))

        # Market Currency 잔고 조정
        if bittrex_marketcurrency_bal / total_marketcurrency_bal > 0.8:
            try:
                transfer_amount = bittrex_marketcurrency_bal - (total_marketcurrency_bal / 2)
                #bitt.withdraw(marketcurrency, transfer_amount, poloniex_marketcurrency_address)
                send_message('withdraw to Poloniex : {0:8f}{1}'.format(transfer_amount, marketcurrency))
            except:
                send_message_with_error('error')
        if poloniex_marketcurrency_bal / total_marketcurrency_bal > 0.8:
            try:
                transfer_amount = poloniex_marketcurrency_bal - (total_marketcurrency_bal / 2)
                #polo.withdraw(marketcurrency, transfer_amount, bittrex_marketcurrency_address)
                send_message('withdraw to Bittrex : {0:8f}{1}'.format(transfer_amount, marketcurrency))
            except:
                send_message_with_error('error')

    # Alt Currency 잔고 확인
    is_altcurrency_transfering = False
    if not is_altcurrency_transfering:
        try:
            bittrex_altcurrency_bal = float(bitt.getbalance(altcurrency)['Available'])
        except:
            bittrex_altcurrency_bal = 0
        try:
            poloniex_altcurrency_bal = float(polo.returnBalances()[altcurrency])
        except:
            poloniex_altcurrency_bal = 0
        total_altcurrency_bal = bittrex_altcurrency_bal + poloniex_altcurrency_bal
        print('bittrex : {0:8f}{1} / poloniex : {2:8f}{3} '.format(bittrex_altcurrency_bal, altcurrency, poloniex_altcurrency_bal, altcurrency))

    # Alt Currency 잔고 조정
    if bittrex_altcurrency_bal / total_altcurrency_bal > 0.8:
        try:
            transfer_amount = bittrex_altcurrency_bal - (total_altcurrency_bal / 2)
            #bitt.withdraw(altcurrency, transfer_amount, poloniex_altcurrency_address)
            send_message('withdraw to Poloniex : {0:8f}{1}'.format(transfer_amount, altcurrency))
        except:
            send_message_with_error('withdraw to Poloniex : {0:8f}{1}'.format(transfer_amount, altcurrency))
    if poloniex_altcurrency_bal / total_altcurrency_bal > 0.8:
        try:
            transfer_amount = poloniex_altcurrency_bal - (total_altcurrency_bal / 2)
            #polo.withdraw(altcurrency, transfer_amount, bittrex_altcurrency_address)
            send_message('withdraw to Bittrex : {0:8f}{1}'.format(transfer_amount, altcurrency))
        except:
            send_message_with_error('withdraw to Bittrex : {0:8f}{1}'.format(transfer_amount, altcurrency))


# 오더북 조회
def getorderbook():
    # Bittrexx 오더북 조회
    #decimal.getcontext().prec = 8
    bittrex_orderbook = bitt.getorderbook(bittrex_market, 'both', 1)
    bittrex_buyorder = bittrex_orderbook['buy']
    bittrex_sellorder = bittrex_orderbook['sell']
    #print(bittrex_orderbook)
    poloniex_orderbook = polo.returnOrderBook(poloniex_market)
    poloniex_buyorder = poloniex_orderbook['bids']
    poloniex_sellorder = poloniex_orderbook['asks']
    #print(poloniex_orderbook)
    '''
    for order in bittrex_buyorder:
        print(float(order['Rate'])*1000) #내림차순
    print("------------------------------------------")
    for order in poloniex_buyorder:   #내림차순
        print(order[0])
    
    for order in bittrex_sellorder:

        print(round(decimal.Decimal(bittrex_sellorder[0]['Rate']), 8)) #오름차순
    #round(decimal.Decimal(order['Rate']), 8)
    #print("------------------------------------------")
    for order in poloniex_sellorder:   #오름차순
        print(decimal.Decimal(order[0]))
    
    print(util.toSatoshi(bittrex_sellorder[0]['Rate']), bittrex_sellorder[0]['Quantity'])
    print(util.toSatoshi(poloniex_buyorder[0][0]), poloniex_buyorder[0][1])
    print(util.toSatoshi(bittrex_sellorder[0]['Rate'] - float(poloniex_buyorder[0][0])))
    '''
    bittrex_current_sell = util.toSatoshi(bittrex_sellorder[0]['Rate'])
    bittrex_current_buy = util.toSatoshi(bittrex_buyorder[0]['Rate'])
    poloniex_current_sell = util.toSatoshi(poloniex_sellorder[0][0])
    poloniex_current_buy = util.toSatoshi(poloniex_buyorder[0][0])
    print('Bittrex buy:', bittrex_current_buy, marketcurrency, 'sell:', bittrex_current_sell, marketcurrency)
    print('Poloniex buy:', poloniex_current_buy, marketcurrency,  'sell:', poloniex_current_sell, marketcurrency)
    print('bitt:polo', 1 - bittrex_current_sell/poloniex_current_buy)
    print('polo:bitt', 1 - bittrex_current_sell / poloniex_current_buy)
    if poloniex_current_buy > bittrex_current_sell and 1 - bittrex_current_sell/poloniex_current_buy > spread:
        #print((1 - (bittrex_current_sell/poloniex_current_buy))*100, "%")
        print(u'💰 Difference : ', round((1 - (bittrex_current_sell / poloniex_current_buy)) * 100, 2), "%", ' / Buy at Bittrex!!')

    if bittrex_current_buy > poloniex_current_sell and 1 - poloniex_current_sell/bittrex_current_buy > spread:
        print(u'💰 Difference : ', round((1 - (poloniex_current_sell / bittrex_current_buy))*100, 2), "%", ' / Buy at Poloniex')

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
    while True:
        try:
            getorderbook()
            time.sleep(10)
        except:
            print("⚠️ Bot paused during 1 min -", sys.exc_info())
            time.sleep(60*1)
            print("🔆 Bot resumed")
