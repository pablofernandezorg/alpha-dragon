#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import insertdata
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
    
from datetime import datetime, timedelta
from urllib.request import urlopen
import json
import random

def price_data(connection, ticker):
    """
    This function can be modified to take different lengths of historical data
    based on what is needed
    
    Returns a nested list in the following format:
    [0] = YYYY - MM - DD
    [1] = Open Price
    [2] = High Price
    [3] = Low Price
    [4] = Closing Price
    [5] = Volume
    [6] = Closing with 1 SigFig Accuracy 
    """
    
    backtrack  = datetime.today() - timedelta(days=5)
    start_date = backtrack.strftime('%Y%m%d')
    end_date   = datetime.datetime.today().strftime('%Y%m%d')
    print("Raw Stock Data Historical Price -----------------------------")
    data = fetch_historical_prices(ticker, start_date, end_date)
    
    counter = 0 
    for historical in data: 
        Date           = historical[0] 
        Open_Price     = historical[1] 
        High_Price     = historical[2] 
        Low_Price      = historical[3] 
        Closing_Price  = historical[4] 
        Volume         = historical[5] 
        Ticker         = ticker
        Unique_Entry   = random.randint(10000, 100000000000000)
        counter = counter + 1
        insertdata.insert_stockprices(counter, connection, Unique_Entry, Date, Open_Price, High_Price, Low_Price, Closing_Price, Volume, Ticker)    
    return data
    
def fetch_historical_prices(symbol, start_date, end_date):
    """
    This function gets historical prices for the given ticker symbol. 
    """
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(end_date[4:6]) - 1) + \
          'e=%s&' % str(int(end_date[6:8])) + \
          'f=%s&' % str(int(end_date[0:4])) + \
          'g=d&' + \
          'a=%s&' % str(int(start_date[4:6]) - 1) + \
          'b=%s&' % str(int(start_date[6:8])) + \
          'c=%s&' % str(int(start_date[0:4])) + \
          'ignore=.csv'
    days = urlopen(url).readlines()    
    data = [day[:-2].decode("ascii").split(',') for day in days][1:]
    return data
    
def fetch_tweets(ticker):
    """
    This function grabs tweets that mention the stock ticket being searched
    """
    url = "https://api.stocktwits.com/api/2/streams/symbol/{0}.json".format(ticker)
    tweets = urlopen(url).read()
    print(type(tweets))
    data = json.loads(tweets.decode('utf-8'))
    return data
    
def get_tweets_list(tickers):
    ret = {}
    for ticker in tickers:
        print ("Getting data for", ticker)
        try:
            data = fetch_tweets(ticker)
            symbol = data['symbol']['symbol']
            msgs = data['messages']
            ret.update({symbol : msgs})
        except Exception as e:
            print (e)
            print ("Error getting", ticker)
    return ret
