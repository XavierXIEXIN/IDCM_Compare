# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:02:49 2018

@author: XavierXIEXIN
"""
import time
import ccxt
import requests
import pandas as pd

EXCHANGE_DIC = {'huobipro': ccxt.huobipro(), 'okex': ccxt.okex(), 'zb': ccxt.zb()}
HUOBI_OTC_BASE = "https://otc-api.huobi.pro/v1/otc/trade/list/public?country=0&currency=1&payMethod=0&currPage=1&merchant=1"
IDCM_OTC_BASE = "http://apic2c.idcm.io:8304/api/Order/GetSaleOrderList?&pageIndex=0&pageSize=10&isOnline=true"

def get_ticker_price(exchange='huobipro', direction='', base_currency='btc', quote_currency='usdt'):
    """
    Get ticker price by exchanges, direction and trading pairs.
    """
    if exchange == 'IDCM':
        pass
    else:
        ex = EXCHANGE_DIC[exchange]
        ex_symbol = base_currency.upper() + '/' + quote_currency.upper()
        ex_orderbook = ex.fetch_order_book(ex_symbol)
        ex_bid = ex_orderbook['bids'][0][0]
        ex_ask = ex_orderbook['asks'][0][0]
        ex_timestamp = ex_orderbook['timestamp']
    if direction =='':
        return [ex_timestamp, ex_bid, ex_ask]
    elif direction == 'buy':
        price = max(ex_bid, ex_ask)
    elif direction == 'sell':
        price = min(ex_bid, ex_ask)
        
    return price

def get_otc_price(exchange='huobipro', direction='', base_currency='usdt', quote_currency='cny'):
    
    if exchange=='huobipro':
        coinId = {'btc':1, 'eth':3, 'usdt':2}
        tradeType = {'buy':1, 'sell':0}
        url_buy = HUOBI_OTC_BASE + '&coinId=' + str(coinId[base_currency]) + '&tradeType=' + str(tradeType['buy'])
        url_sell = HUOBI_OTC_BASE + '&coinId=' + str(coinId[base_currency]) + '&tradeType=' + str(tradeType['sell'])
        buy_data = requests.get(url_buy).json()
        sell_data = requests.get(url_sell).json()
        otc_bid = sell_data['data'][0]['fixedPrice']
        otc_ask = buy_data['data'][0]['fixedPrice']
        otc_timestamp = int(time.time() * 1000)
        
        return [otc_timestamp, otc_bid, otc_ask]

    elif exchange=='IDCM':
        tradeSide = {'buy':1, 'sell':0}
        url_buy = IDCM_OTC_BASE + '&coinCode=' + base_currency.upper() + '&currencyCode=' + quote_currency.upper() + '&tradeSide=' + str(tradeSide['buy'])
        url_sell = IDCM_OTC_BASE + '&coinCode=' + base_currency.upper() + '&currencyCode=' + quote_currency.upper() + '&tradeSide=' + str(tradeSide['sell'])
        buy_data = requests.post(url_buy).json()
        sell_data = requests.post(url_sell).json()
        otc_bid = sell_data['Data'][0]['Price']
        otc_ask = buy_data['Data'][0]['Price']
        otc_timestamp = int(time.time() * 1000)
        
        return [otc_timestamp, otc_bid, otc_ask]
        
if __name__ == '__main__' :

    btc_ticker_price = pd.DataFrame(index = ['timestamp', 'bid', 'ask'])
    for ex in EXCHANGE_DIC.keys():
        btc_ticker_price[ex] = get_ticker_price(exchange=ex)
        
    eth_ticker_price = pd.DataFrame(index = ['timestamp', 'bid', 'ask'])
    for ex in EXCHANGE_DIC.keys():
        eth_ticker_price[ex] = get_ticker_price(exchange=ex, base_currency='eth')
        
    usdt_c2c_price = pd.DataFrame(index = ['timestamp', 'bid', 'ask'])
    for ex in ['huobipro']:
        usdt_c2c_price[ex] = get_otc_price(exchange=ex)

    vhkd_c2c_price = pd.DataFrame(index = ['timestamp', 'bid', 'ask'])
    for ex in ['IDCM']:
        vhkd_c2c_price[ex] = get_otc_price(exchange=ex, base_currency='vhkd')
        
    btc_c2c_price = pd.DataFrame(index = ['timestamp', 'bid', 'ask'])
    for ex in ['huobipro']:
        btc_c2c_price[ex] = get_otc_price(exchange=ex, base_currency='btc')

    eth_c2c_price = pd.DataFrame(index = ['timestamp', 'bid', 'ask'])
    for ex in ['huobipro']:
        eth_c2c_price[ex] = get_otc_price(exchange=ex, base_currency='eth')

    writer = pd.ExcelWriter('price.xlsx')

    btc_ticker_price.to_excel(writer, 'btc_ticker_price')
    eth_ticker_price.to_excel(writer, 'eth_ticker_price')

    usdt_c2c_price.to_excel(writer, 'usdt_c2c_price')
    vhkd_c2c_price.to_excel(writer, 'vhkd_c2c_price')
    btc_c2c_price.to_excel(writer, 'btc_c2c_price')
    eth_c2c_price.to_excel(writer, 'eth_c2c_price')

    writer.save()
    
    