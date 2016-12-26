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

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
 
import analysis
import update

def pull_tweets_not_analyzed(connection):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `StockTweets` WHERE `Tweet_Sentiment`='0' ORDER BY RAND() LIMIT 100" 
        cursor.execute(sql, ())
        connection.commit()
        result = cursor.fetchall()
        numrows = cursor.rowcount
        
    for row in result:
        ticker_symbol = row["Ticker"]
        score = analysis.sentiment_analysis_ultra(row["Tweet_Content"], row["User_Sentiment"], row["Unique_Entry"])
        unique_entry = row["Unique_Entry"]
        status = update.update_analysis(connection, unique_entry, score)
        if(status == "Success"):
            print("Updated Analysis")    
        update.last_analysis(connection, ticker_symbol)
    
def pull_active_stocks(connection):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `Stocks` WHERE `Status`='Active' ORDER BY RAND() LIMIT 50" 
        cursor.execute(sql, ())
        connection.commit()
        stocks = cursor.fetchall()
    return stocks