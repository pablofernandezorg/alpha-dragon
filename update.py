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

from datetime import datetime, timedelta
import os, time

os.environ['TZ'] = 'America/Los_Angeles'
time.tzset()

def update_analysis(connection, unique_entry, score):
    cursor = connection.cursor()
    sql = "UPDATE StockTweets SET Tweet_Sentiment='%s' WHERE Unique_Entry='%s'"
    cursor.execute(sql, (score, unique_entry))
    connection.commit()
    return "Success"
    
def update_stockprices(connection, Date, Open_Price, High_Price, Low_Price, Closing_Price, Volume, Ticker):
    cursor = connection.cursor()
    sql = "UPDATE StockPrices SET Open_Price=%s WHERE Date=%s AND Ticker=%s"
    cursor.execute(sql, (Open_Price, Date, Ticker))
    connection.commit()

    cursor = connection.cursor()
    sql = "UPDATE StockPrices SET High_Price=%s WHERE Date=%s AND Ticker=%s"
    cursor.execute(sql, (High_Price, Date, Ticker))
    connection.commit()
    
    cursor = connection.cursor()
    sql = "UPDATE StockPrices SET Low_Price=%s WHERE Date=%s AND Ticker=%s"
    cursor.execute(sql, (Low_Price, Date, Ticker))
    connection.commit()
    
    cursor = connection.cursor()
    sql = "UPDATE StockPrices SET Closing_Price=%s WHERE Date=%s AND Ticker=%s"
    cursor.execute(sql, (Closing_Price, Date, Ticker))
    connection.commit()
    
    cursor = connection.cursor()
    sql = "UPDATE StockPrices SET Volume=%s WHERE Date=%s AND Ticker=%s"
    cursor.execute(sql, (Volume, Date, Ticker))
    connection.commit()
    return "Success"
    
def last_fetch(connection, ticker):
    date_check  = datetime.today() - timedelta(days=0)
    today       = date_check.strftime('%H:%M:%S %m-%d-%Y')                
    cursor = connection.cursor()
    sql = "UPDATE Stocks SET Last_Fetch=%s WHERE Ticker=%s"
    cursor.execute(sql, (today, ticker))
    connection.commit()
    return "Success"

def last_analysis(connection, ticker):
    date_check  = datetime.today() - timedelta(days=0)
    today       = date_check.strftime('%H:%M:%S %m-%d-%Y')                
    cursor = connection.cursor()
    sql = "UPDATE Stocks SET Last_Analysis=%s WHERE Ticker=%s"
    cursor.execute(sql, (today, ticker))
    connection.commit()
    return "Success"
    
def last_input(connection, ticker):
    date_check  = datetime.today() - timedelta(days=0)
    today       = date_check.strftime('%H:%M:%S %m-%d-%Y')                
    cursor = connection.cursor()
    sql = "UPDATE Stocks SET Last_Input=%s WHERE Ticker=%s"
    cursor.execute(sql, (today, ticker))
    connection.commit()
    return "Success"

def last_prices(connection, ticker):
    date_check  = datetime.today() - timedelta(days=0)
    today       = date_check.strftime('%H:%M:%S %m-%d-%Y')                
    cursor = connection.cursor()
    sql = "UPDATE Stocks SET Last_Prices=%s WHERE Ticker=%s"
    cursor.execute(sql, (today, ticker))
    connection.commit()
    return "Success"
    
def month_pulls_basic(connection, ticker):
    cursor = connection.cursor()
    sql = "UPDATE Stocks SET Month_Pulls_Basic = Month_Pulls_Basic+1 WHERE Ticker=%s"
    cursor.execute(sql, (ticker))
    connection.commit()
    return "Success"
    
def month_pulls_pro(connection, ticker):
    cursor = connection.cursor()
    sql = "UPDATE Stocks SET Month_Pulls_Pro = Month_Pulls_Pro+1 WHERE Ticker=%s"
    cursor.execute(sql, (ticker))
    connection.commit()
    return "Success"
    
def month_pulls_ultra(connection, ticker):
    cursor = connection.cursor()
    sql = "UPDATE Stocks SET Month_Pulls_Ultra = Month_Pulls_Ultra+1 WHERE Ticker=%s"
    cursor.execute(sql, (ticker))
    connection.commit()
    return "Success"
    
def large_moving_avg(connection, avg, ticker):
    cursor = connection.cursor()
    sql = "UPDATE Stocks SET LongMovingAvg = %s WHERE Ticker=%s"
    cursor.execute(sql, (avg, ticker))
    connection.commit()
    return "Success"
    
def small_moving_avg(connection, avg, ticker):
    cursor = connection.cursor()
    sql = "UPDATE Stocks SET ShortMovingAvg = %s WHERE Ticker=%s"
    cursor.execute(sql, (avg, ticker))
    connection.commit()
    return "Success"

def avg_volume_long(connection, avg, ticker):
    cursor = connection.cursor()
    sql = "UPDATE Stocks SET AvgVolumeNinety = %s WHERE Ticker=%s"
    cursor.execute(sql, (avg, ticker))
    connection.commit()
    return "Success"
    
def avg_sentiment_short(connection, avg, ticker):
    cursor = connection.cursor()
    sql = "UPDATE Stocks SET AvgSentimentThirty = %s WHERE Ticker=%s"
    cursor.execute(sql, (avg, ticker))
    connection.commit()
    return "Success"
    
def avg_tweets_short(connection, avg, ticker):
    cursor = connection.cursor()
    sql = "UPDATE Stocks SET AvgTweetVolumeThirty = %s WHERE Ticker=%s"
    cursor.execute(sql, (avg, ticker))
    connection.commit()
    return "Success"
    
def today_tweets(connection, num, ticker):
    cursor = connection.cursor()
    sql = "UPDATE Stocks SET Tweets = %s WHERE Ticker=%s"
    cursor.execute(sql, (num, ticker))
    connection.commit()
    return "Success"