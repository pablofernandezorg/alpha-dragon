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
import update
import pulldata
import connection

def main():
    connect     = connection.connection()
    ticker_list = []
    active      = pulldata.pull_active_stocks(connect)
                        
    for stock in active:
        ticker = stock["Ticker"].rstrip()
        ticker_list.append(ticker)       
        
    for ticker_sybmbol in ticker_list:
        total_count = 0.00001
        
        total_corct = 0    
        corct_perct = 0
            
        total_incrt = 0
        incrc_perct = 0
        
        total_neutr = 0
        

        result = pulldata.pull_neural_predictions(connect, ticker_sybmbol)
        
        for item in result:
            occured = item["Result"]
            tickrrr = item["Ticker"]

            if(occured=="Correct"):
                total_corct +=1
                total_count +=1
            elif(occured=="Incorrect"):
                total_incrt +=1
                total_count +=1
            elif(occured=="Neutral"):
                total_neutr +=1
            else:
                sys.exit("Fatal Error")
                
            corct_perct = ((total_corct / total_count) * 100)
            if((total_corct==0) and (total_incrt==0)):
                corct_perct = -0.01
                
            incrc_perct = ((total_incrt / total_count) * 100)

        print("Ticker: ", tickrrr)
        print("Correct:     ", total_corct, "/", total_count, "  ", corct_perct, "%")
        print("Incorrect:   ", total_incrt, "/", total_count, "  ", incrc_perct, "%")
        print("Neutral:     ", total_neutr)
        
        corct_perct = round(corct_perct, 2)
        update.prediction_accuracy(connect, corct_perct, tickrrr)
        

    print("*********** Program Completed ***********")
    
if __name__ == "__main__":
    main()                