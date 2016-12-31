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

import connection

def main():
    pre = 0
    connect = connection.connection()

    with connect.cursor() as cursor:
        sql = "SELECT * FROM `StockTweets` ORDER BY Date" 
        cursor.execute(sql, ())
        connect.commit()
        result = cursor.fetchall()
        numrows = cursor.rowcount

    Dates = []
    for row in result:
        Date = row["Date"]
        
        if Date in Dates:
            pre = 0 # This does nothing
        else:
            Dates.append(Date)
            
    for Date in Dates:
        db = {}
        stock = []
        with connect.cursor() as cursor:
            sql = "SELECT * FROM `StockTweets` WHERE Date=%s" 
            cursor.execute(sql, (Date))
            connect.commit()
            resultinputs = cursor.fetchall()
            numrows = cursor.rowcount

        print("Current Date", Date)  
        
        for Input in resultinputs:
            Tick = Input["Ticker"]
            if Tick in db:
                db[Tick] += 1
            else:
                db[Tick] = 0 

        for each in db:
            val = db[each]
            
            with connect.cursor() as cursor:
                quer = "SELECT * FROM `Stocks` WHERE Ticker=%s" 
                cursor.execute(quer, (each))
                connect.commit()
                avgresult = cursor.fetchall()
            
            for Resulting in avgresult:
                vol = Resulting["AvgTweetVolumeThirty"]
                vol = float(vol) 
                vol = round(vol,0)
                
            if(val<(0.70*vol)):
                pre = 0 # This does nothing
                #print("Low Volume For", each)
            else:
                stock.append(each)
        
        print(stock)    
        
    
if __name__ == "__main__":
    main()

"""


"""