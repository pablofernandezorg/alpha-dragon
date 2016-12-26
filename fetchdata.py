#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
******************************************************************************
Intellecutal Property Notice:

The following confidential program contains algorithms written by Pablo Fernandez
that may eventually be sold or used in a commerical setting. 

Please do not share or distribute this program. Copyright 2016. 

Thank you.
Pablo Fernandez
www.pablofernandez.com
******************************************************************************
"""

import insertdata
import modify
import update

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
    end_date   = datetime.today().strftime('%Y%m%d')
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
    
    
def fetch_saved_tweets(connection, filename, ticker, ticker_company):
    with open(filename) as data_file:    
        data = json.load(data_file)

    position = 0
    position = int(position)
    list_size = len(data[ticker])

    for tweet in range(0,list_size):
        Unique_Entry        = data[ticker][position]["id"]
        Date                = data[ticker][position]["created_at"]
        Date                = Date.split("T")[0]
        Date                = Date.split("-")
        Date                = Date[0] + "-" + Date[1] + "-" + Date[2]
        User_Sentiment      = data[ticker][position]["entities"]["sentiment"]
        if User_Sentiment is not None:
            User_Sentiment = User_Sentiment["basic"]
        if 'likes' in data[ticker][position]:
            Total_Likes     = data[ticker][position]["likes"]["total"]
        else:
            Total_Likes     = 0
        Username            = data[ticker][position]["user"]["username"]
        Tweet_Content       = data[ticker][position]["body"]
        
        Tweet_Sentiment     = "0"
        Tweet_Analysis      = "0"
        Ticker              = ticker
        
        position = position + 1
        
        print("")
        print(ticker_company)        
        print("----------------------------- Tweet: ", position)
        print("Entry         ", Unique_Entry)        
        print("Date:         ", Date)
        print("Total Likes:  ", Total_Likes)
        print("Username:     ", Username)
        print("Tweet Body:   ", Tweet_Content)
        print("----------------------------- ")

        Tweet_Content = connection.escape(Tweet_Content)
        Tweet_Content = modify.sanitize_data(Tweet_Content)
        insertdata.insert_database(connection, Unique_Entry, Date, User_Sentiment, Total_Likes, Username, Tweet_Content, Tweet_Sentiment, Tweet_Analysis, Ticker)
    
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