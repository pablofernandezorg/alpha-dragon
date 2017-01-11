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
import csv
import pulldata
import os


def main():
    connect     = connection.connection()
    ticker_list = []
    active      = pulldata.pull_active_stocks(connect)
                        
    for stock in active:
        ticker = stock["Ticker"].rstrip()
        ticker_list.append(ticker)       
    
    for ticker in ticker_list:
        with open('../alphadragon/data/candlestick%s.csv' % ticker, 'w') as candlestick:
            wr   = csv.writer(candlestick, quoting=csv.QUOTE_ALL)
            data = pulldata.pull_candlestickgraph(connect, ticker)
            for elements in data:
                Package       = []
                Date          = elements['Date']
                Package.append(Date)
                Open_Price    = elements['Open_Price']
                Package.append(Open_Price)
                High_Price    = elements['High_Price']
                Package.append(High_Price)
                Low_Price     = elements['Low_Price']
                Package.append(Low_Price)
                Closing_Price = elements['Closing_Price']
                Package.append(Closing_Price)
                Volume        = elements['Volume']
                Package.append(Volume)                
                if Closing_Price is not None:  
                    wr.writerow(Package)
            os.chmod('candlestick%s.csv' % ticker, 0o700)

    for ticker in ticker_list:
        with open('../alphadragon/data/linearprice%s.csv' % ticker, 'w') as linearprice:
            wr   = csv.writer(linearprice, quoting=csv.QUOTE_ALL)
            data = pulldata.pull_lineargraph(connect, ticker)
            for elements in data:
                Package       = []
                Date          = elements['Date']
                Package.append(Date)
                Closing_Price = elements['Closing_Price']
                Package.append(Closing_Price)
                if Closing_Price is not None:  
                    wr.writerow(Package)
        os.chmod('linearprice%s.csv' % ticker, 0o700)


    print("*********** Program Completed ***********")
    
if __name__ == "__main__":
    main()                