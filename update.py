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

def update_analysis(connection, unique_entry, score):
    cursor = connection.cursor()
    sql = "UPDATE StockTweets SET Tweet_Sentiment='%s' WHERE Unique_Entry='%s'"
    cursor.execute(sql, (score, unique_entry))
    connection.commit()
    return "Success"
            