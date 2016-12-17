#!/usr/local/bin/python
# -*- coding: utf-8 -*-

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import modify

def insert_database(connection, Unique_Entry, Date, User_Sentiment, Total_Likes, Username, Tweet_Content, Tweet_Sentiment, Tweet_Analysis, Ticker):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `StockTweets` WHERE `Unique_Entry`=%s"
            cursor.execute(sql, (Unique_Entry))
            result = cursor.fetchone()
            
        if result is None:
            print("Success: Inserting Into Database", Ticker)
            Tweet_Content = connection.escape(Tweet_Content)
            Tweet_Content = modify.remove_emoji(Tweet_Content)
            with connection.cursor() as cursor:
                sql = "INSERT INTO `StockTweets` (`Unique_Entry`, `Date`, `User_Sentiment`, `Total_Likes`, `Username`, `Tweet_Content`, `Tweet_Sentiment`, `Tweet_Analysis`, `Ticker`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (Unique_Entry, Date, User_Sentiment, Total_Likes, Username, Tweet_Content, Tweet_Sentiment, Tweet_Analysis, Ticker))
                connection.commit()
        else:
            print("Error: Duplicate Entry", Ticker)
    
    finally:
        print("DO NOT CLOSE CONNECTION")
        #connection.close()
        
def insert_stockprices(counter, connection, Unique_Entry, Date, Open_Price, High_Price, Low_Price, Closing_Price, Volume, Ticker):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `StockPrices` WHERE `Date`=%s AND `Ticker`=%s" 
            cursor.execute(sql, (Date, Ticker))
            result = cursor.fetchone()
            
        if result is None:
            print("Success: Inserting Into Database", Ticker, " - " ,counter)
            with connection.cursor() as cursor:
                sql = "INSERT INTO `StockPrices` (`Unique_Entry`, `Date`, `Open_Price`, `High_Price`, `Low_Price`, `Closing_Price`, `Volume`, `Ticker`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (Unique_Entry, Date, Open_Price, High_Price, Low_Price, Closing_Price, Volume, Ticker))
                connection.commit()
        else:
            print("Error: Duplicate Entry", Ticker)
            
    finally:
        print("DO NOT CLOSE CONNECTION")
        #connection.close()
