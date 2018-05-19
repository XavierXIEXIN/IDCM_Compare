# -*- coding: utf-8 -*-
"""
Created on Sat May 19 16:51:21 2018

@author: xx
"""

import pandas as pd
import ccxt

ALTS = ["BCH",
"BTG",
"ETH",
"XRP",
"LTC",
"ETC",
"TRX",
"OMG",
"SNT",
"ZRX",
"KNC",
"BAT",
"FUN",
"EOS",
]
ALTS2 = ["SALT"]
#SYMBOLS = [x+"/BTC" for x in ALTS]

exchange = ccxt.bitfinex2()
#markets = exchange.load_markets()
df = pd.DataFrame(columns=['BTC PRICE', 'TIME'])
for alt in ALTS:
    symbol = alt + "/BTC"
    ticker_data = exchange.fetch_ticker(symbol)
    df.loc[alt] = [ticker_data['last'], ticker_data['datetime']]
    
exchange2 = ccxt.binance()
for alt in ALTS2:
    symbol = alt + "/BTC"
    ticker_data = exchange2.fetch_ticker(symbol)
    df.loc[alt] = [ticker_data['last'], ticker_data['datetime']]

df.to_excel("Alts_BTC_price"+str(ticker_data['timestamp'])+".xlsx")
