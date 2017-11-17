#-*- coding: utf-8 -*-
import config
from bittrex import bittrex
from poloniex import poloniex

##변수선언
marketcurrency = 'BTC'  #기준코인
altcurrency = 'DGB' #알트코인
spread = 0.8  #차이 1% => 1
market_bitt = '{0}-{1}'.format(marketcurrency, altcurrency)
market_polo = '{0}_{1}'.format(marketcurrency, altcurrency)
is_marketcurrency_transfering = False
is_altcurrency_transfering = False
bittrex_api = config.bittrex_api
bittrex_key = config.bittrex_key
poloniex_api = config.poloniex_api
poloniex_key = config.poloniex_key

##API 객채생성
bitt = bittrex(bittrex_api, bittrex_key)
polo = poloniex(poloniex_api, poloniex_key)


def balancing():
    ##1. 잔고조정
    #1-1. 잔고 조회
    bitt_marketcurrency_bal = 0
    polo_marketcurrency_bal = 0
    try:
        bitt_marketcurrency_bal = float(bitt.getbalance(marketcurrency)['Available'])
    except:
        bitt_marketcurrency_bal = 0
    try:
        polo_marketcurrency_bal = float(polo.returnBalances()[marketcurrency])
    except:
        polo_marketcurrency_bal = 0

    total_marketcurrency_bal = bitt_marketcurrency_bal + polo_marketcurrency_bal

    #to-do:이체 내역 존재여부 확인
    '''
    #이체내역이 존재하지 않으면
    if not is_marketcurrency_transfering:

        if bitt_btc_bal / total_btc_bal > 0.7 : #bittrex의BTC가 전체 BTC의 70%를 초과할때
            #이체금액 계산
            print('polo로 이체')

        if polo_btc_bal / total_btc_bal > 0.7 : #poloniex의BTC가 전체 BTC의 70%를 초과할때
            print('bitt로 이체')
    '''
    print(bitt_marketcurrency_bal, polo_marketcurrency_bal)



##오더북 조회

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
    balancing()
