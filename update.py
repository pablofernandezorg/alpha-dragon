#!/usr/local/bin/python
# -*- coding: utf-8 -*-

def update_analysis(connection, unique_entry, score):
    cursor = connection.cursor()
    sql = "UPDATE StockTweets SET Tweet_Sentiment='%s' WHERE Unique_Entry='%s'"
    cursor.execute(sql, (score, unique_entry))
    connection.commit()
    return "Success"
            
