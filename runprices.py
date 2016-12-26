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
import fetchdata
import pulldata
import connection
import pprint

def main():
    connect     = connection.connection()
    ticker_list = []
    active      = pulldata.pull_active_stocks(connect)
                        
    for stock in active:
        ticker = stock["Ticker"].rstrip()
        ticker_list.append(ticker)
                
    for ticker_sybmbol in ticker_list:
        result = fetchdata.price_data(connect, ticker_sybmbol)
        pprint.pprint(result)
    print("*********** Program Completed ***********")
    
if __name__ == "__main__":
    main()                