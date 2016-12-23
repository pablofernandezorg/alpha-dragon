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

"""
Modules
-----------------------------------------------------
modify        #    Parsing Twitter Input Values
analysis      #    **CONFIDENTIAL Scoring Algorithm For Language & Trends
connection    #    **CONFIDENTIAL Server Database Authentication & Connection
fetchdata     #    Fetch Data From Twitter & Yahoo Finance 
pulldata      #    Pull Any Sort Of Information From The Database
insertdata    #    Insert Tweets & Stock Prices Into Database
update        #    Push Any Sort Of Update To The Database

Cron Jobs
-----------------------------------------------------
Currently tracking 47 stocks every 15 mins on /home/pablofernandez/public_html/cgi-bin/stocktwits.py
Remove garbage tweets every hour  /public_html/stockmarket/update_http_broken_tweets.php


Neural Network
Data Set

[1, 5]                 - Day of Week (Seasonality, Numerical)
[1, 23]                - Trading Day (Seasonality, Numerical)
[1, 12]                - Month (Seasonality, Numerical)
[0, 20]                - Volume (% Difference From Average, Normalized In Percentiles)
[0, 1]  False / True   - Above the 200 Day Moving Average (Normally Bullish Indicator)
[0, 1]  False / True   - Below the 5 Day Moving Average (Normally Bullish Indicator)
[0, 20]                - % Above / Below the 5 Day Moving Average (Normally Lower The Better, 5% Lowest Values Recorded Over X Months, Normalized In Percentiles)
[0, 10]                - Headlines And Commotion In The News
[0, 20]                - % Above / Below the Average Twitter Volume For That Stock
[0, 200]               - Sentiment Analysis (Check back for liked Tweets and add credibility to magnify (-/+) score x0.15)

Goal  
[0, 3]    - Stock went down
[1, 4]    - Neutral  (Change less then 1%)
[2, 5]    - Stock went up
"""

import fetchdata
import pulldata
import connection

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
   
import json
import datetime
import pprint

FILENAME = "tweetdata.json" 
        
def append_no_duplicates(original, msgs):
    print ("Appending tweets")
    for ticker in msgs.keys():
        if ticker not in original.keys():
            original[ticker] = msgs[ticker]
        else:
            for msg in msgs[ticker]:
                if msg not in original[ticker]: # check for duplicates
                    original[ticker].append(msg)
    return original

def cull_age_limit(original, age_limit=30):
    # cull all tweets over age_limit days old
    print ("Culling tweets that are more than", age_limit, "days old")
    threshold = datetime.datetime.now() - datetime.timedelta(age_limit)
    result = {}
    for ticker in original.keys():
        result[ticker] = []
        for msg in original[ticker]:
            dt = datetime.datetime.strptime(msg["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if dt >= threshold:
                result[ticker].append(msg)
    return result

def read_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def write_to_file(filename, d):
    with open(filename, 'w+') as f:
        print ("Dumping JSON to", filename)
        json.dump(d, f)

def erase_temporary_file(filename):
    open(filename, 'w').close()
                
def main():
    connect     = connection.connection()
    ticker_list = []
    active      = pulldata.pull_active_stocks(connect)
                        
    for stock in active:
        ticker = stock["Ticker"]
        ticker_list.append(ticker)
        
    for ticker_sybmbol in ticker_list:
        result = fetchdata.price_data(connect, ticker_sybmbol)
        pprint.pprint(result)    

    new = fetchdata.get_tweets_list(ticker_list)
    new = cull_age_limit(new)
    write_to_file(FILENAME, new)
    
    for ticker_sybmbol in ticker_list:
        fetchdata.fetch_saved_tweets(connect, FILENAME, ticker_sybmbol)

    for ticker_sybmbol in ticker_list:
        pulldata.pull_tweets_not_analyzed(connect, ticker_sybmbol)
                
    erase_temporary_file(FILENAME)
    connect.close()
    
if __name__ == "__main__":
    main()