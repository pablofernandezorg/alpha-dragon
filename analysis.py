#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import requests

positive_words = ["great", "positive", "bullish", "rising", "short squeeze", "successful", "long", "buy", "bought", "call", "profit", "buy rating"]
negative_words = ["bleed", "crap", "drop", "bearish", "falling", "terrible", "sad", "poor", "negative", "plumet", "sell", "sold", "puts", "junk", "failure"]

def tweet_analysis(content, hint, entry):
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
    return total_score   
