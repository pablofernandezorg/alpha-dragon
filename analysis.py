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

import requests

    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************

positive_words = ["great", "positive", "bullish", "rising", "short squeeze", "successful", "long", "buy", "bought", "call", "profit", "buy rating"]
negative_words = ["bleed", "crap", "drop", "bearish", "falling", "terrible", "sad", "poor", "negative", "plumet", "sell", "sold", "puts", "junk", "failure"]

def sentiment_analysis_ultra(content, hint, entry, ticker_symbol):                            
    url     = "https://japerk-text-processing.p.mashape.com/sentiment/"
    payload = { 'text' : content , 'language' : 'english' }
    headers = { 'X-Mashape-Key' : 'gUG3dwBilimshEMaMrYCY1cE1AW9p1b4zryjsne7zNuvHMKi0H' , 'Content-Type' : 'application/x-www-form-urlencoded', 'Accept' : 'application/json'}
    res = requests.post(url, data=payload, headers=headers)
    result = res.json()
    total_score = 0
    positive = result["probability"]["pos"]
    positive = positive * 100
    negative = result["probability"]["neg"]
    negative = negative * 100
    neutral  = result["probability"]["neutral"] 
    neutral  = neutral * 100
    if(hint=="Bearish"):
        total_score = total_score - negative # Add More Weight Due To Negative Sentiment
    elif(hint=="Bullish"):
        total_score = total_score + positive # Add More Weight Due To Positive Sentiment
    else:
        total_score = total_score + positive - negative # If Sentiment Unkown, Average Score
        
    total_score = round(total_score, 0)
    if((total_score == 0.0) or (total_score == 0)):
        total_score = 0.01 
    
    print("----------------------------------------------------------------")
    print("Score Analysis:       ", total_score, " Entry: ", entry)
    print("Positive:       ", positive)
    print("Negative:       ", negative)
    print("Neutral:        ", neutral)
    
    update.month_pulls_ultra(connection, ticker_symbol)
    return total_score

def sentiment_analysis_pro(content, hint, entry, ticker_symbol):                            
    url     = "https://japerk-text-processing.p.mashape.com/sentiment/"
    payload = { 'text' : content , 'language' : 'english' }
    headers = { 'X-Mashape-Key' : 'yeJu4D3OAxmshiWcaCQTUmaNJP6Wp1ezvrGjsnboefFhsLgc5c' , 'Content-Type' : 'application/x-www-form-urlencoded', 'Accept' : 'application/json'}
    res = requests.post(url, data=payload, headers=headers)
    result = res.json()
    total_score = 0
    positive = result["probability"]["pos"]
    positive = positive * 100
    negative = result["probability"]["neg"]
    negative = negative * 100
    neutral  = result["probability"]["neutral"] 
    neutral  = neutral * 100
    if(hint=="Bearish"):
        total_score = total_score - negative # Add More Weight Due To Negative Sentiment
    elif(hint=="Bullish"):
        total_score = total_score + positive # Add More Weight Due To Positive Sentiment
    else:
        total_score = total_score + positive - negative # If Sentiment Unkown, Average Score
        
    total_score = round(total_score, 0)
    if((total_score == 0.0) or (total_score == 0)):
        total_score = 0.01 
    
    print("----------------------------------------------------------------")
    print("Score Analysis:       ", total_score, " Entry: ", entry)
    print("Positive:       ", positive)
    print("Negative:       ", negative)
    print("Neutral:        ", neutral)
    
    update.month_pulls_pro(connection, ticker_symbol)
    return total_score
    
def sentiment_analysis_basic(content, hint, entry, ticker_symbol):
    url     = "http://text-processing.com/api/sentiment/"
    payload = { 'text' : content }
    headers = {}
    res = requests.post(url, data=payload, headers=headers)
    result = res.json()
    total_score = 0
    positive = result["probability"]["pos"]
    positive = positive * 100
    negative = result["probability"]["neg"]
    negative = negative * 100
    neutral  = result["probability"]["neutral"] 
    neutral  = neutral * 100
    if(hint=="Bearish"):
        total_score = total_score - negative # Add More Weight Due To Negative Sentiment
    elif(hint=="Bullish"):
        total_score = total_score + positive # Add More Weight Due To Positive Sentiment
    else:
        total_score = total_score + positive - negative # If Sentiment Unkown, Average Score
        
    total_score = round(total_score, 0)
    if((total_score == 0.0) or (total_score == 0)):
        total_score = 0.01 
    
    print("----------------------------------------------------------------")
    print("Score Analysis:       ", total_score, " Entry: ", entry)
    print("Positive:       ", positive)
    print("Negative:       ", negative)
    print("Neutral:        ", neutral)
    
    update.month_pulls_basic(connection, ticker_symbol)
    return total_score
    
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************
    #**************************** CONFIDENTIAL INFORMATION **************************    
