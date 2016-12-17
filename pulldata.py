#!/usr/local/bin/python
# -*- coding: utf-8 -*-

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
 
import analysis
import json
import insertdata
import update

def fetch_saved_tweets(connection, filename, ticker):
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
        print("----------------------------- Tweet: ", position)
        print("Entry    :    ", Unique_Entry)        
        print("Date:         ", Date)
        print("Total Likes:  ", Total_Likes)
        print("Username:     ", Username)
        print("Tweet Body:   ", Tweet_Content)
        
        insertdata.insert_database(connection, Unique_Entry, Date, User_Sentiment, Total_Likes, Username, Tweet_Content, Tweet_Sentiment, Tweet_Analysis, Ticker)

def pull_tweets_not_analyzed(connection, ticker):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `StockTweets` WHERE `Ticker`=%s AND `Tweet_Sentiment`='0'" 
        cursor.execute(sql, (ticker))
        connection.commit()
        result = cursor.fetchall()
        numrows = cursor.rowcount
        
    for row in result:
        score = analysis.tweet_analysis(row["Tweet_Content"], row["User_Sentiment"], row["Unique_Entry"])
        unique_entry = row["Unique_Entry"]
        status = update.update_analysis(connection, unique_entry, score)
        if(status == "Success"):
            print("Updated Entry")
