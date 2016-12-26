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
analysis      #    Scoring Algorithm For Language & Trends
connection    #    **CONFIDENTIAL Server Database Authentication & Connection
fetchdata     #    Fetch Data From Twitter & Yahoo Finance 
pulldata      #    Pull Any Sort Of Information From The Database
insertdata    #    Insert Tweets & Stock Prices Into Database
update        #    Push Any Sort Of Update To The Database

Cron Jobs
-----------------------------------------------------
Currently tracking 47 stocks every 15 mins on /home/pablofernandez/public_html/cgi-bin/stocktwits.py
Remove garbage tweets every hour  /public_html/stockmarket/update_http_broken_tweets.php
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
    print ("Deleting tweets that are more than", age_limit, "days old")
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
        ticker = stock["Ticker"].rstrip()
        ticker_list.append(ticker)
          
    new = fetchdata.get_tweets_list(ticker_list)
    new = cull_age_limit(new)
    write_to_file(FILENAME, new)
    
    for stock in active:
        ticker_sybmbol = stock["Ticker"].rstrip()
        ticker_company = stock["Company"].rstrip()
        fetchdata.fetch_saved_tweets(connect, FILENAME, ticker_sybmbol, ticker_company)
                
    erase_temporary_file(FILENAME)
    connect.close()
    print("*********** Program Completed ***********")
    
if __name__ == "__main__":
    main()