#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
******************************************************************************
Intellecutal Property Notice:

The following confidential program contains algorithms written by Pablo Fernandez
that may eventually be sold or used in a commercial setting. 

Please do not share or distribute this program. Copyright 2016. 

Thank you.
Pablo Fernandez
www.pablofernandez.com
******************************************************************************
"""

import connection

from datetime import date, datetime, timedelta
import random
import sys

from layer import Layer
from neuron import Neuron
from network import Network
import random

def rangedatelist(date, delta):
    start_date     = datetime.strptime(date, '%Y-%m-%d')
    backtrack      = start_date - timedelta(days=delta)
    back_date      = backtrack.strftime('%Y-%m-%d')
    back_date      = datetime.strptime(back_date, '%Y-%m-%d')
    difference_backtrack = start_date - back_date
    days_list = []
    for i in range(difference_backtrack.days + 1):
        result = (back_date + timedelta(days=i)) 
        days_list.append(result)
    return days_list

def neuralcalculations(connection, ticker, date):    
    try:
        network = Network.load("neuralnetwork.json")
    except Exception as e:
        print("#101 Error: Neural Network Does Not Exist")
        sys.exit("Fatal Error") # Kill Program, Bad User Input

    date_parts = date.split("-") # Explode Date
    year       = date_parts[0]   # Grab The Date
    month      = date_parts[1]   # Grab The Date
    day        = date_parts[2]   # Grab The Date
    Today                        = datetime.today().strftime('%Y-%m-%d') # Grab Todays Date
    Entry                        = random.randint(2000000000,60000000000) 
    DayOfWeek                    = day     # Day of Week
    TickerSymbol                 = ticker  # Ticker Symbol 
    
    day_name   = datetime.strptime((date), '%Y-%m-%d').strftime('%A') # Grab Name of Requested Date
    trading_day = 0
    if(day_name=="Monday"):
        trading_day = 0.2
    elif(day_name=="Tuesday"):
        trading_day = 0.4
    elif(day_name=="Wednesday"):
        trading_day = 0.6
    elif(day_name=="Thursday"):
        trading_day = 0.8
    elif(day_name=="Friday"):
        trading_day = 1
    else:
        print("#102 Fatal Error: Invalid Date Input Received") # Kill Program, Request Not Allowed
        sys.exit("Fatal Error")
            
    print(month)
    if((month=="03") or (month=="04") or (month=="05")):
        trading_season = 0.25
    elif((month=="06") or (month=="07") or (month=="08")):
        trading_season = 0.50
    elif((month=="09") or (month=="10") or (month=="11")):
        trading_season = 0.75
    elif((month=="12") or (month=="01") or (month=="02")):
        trading_season = 1.0
    else:
        print("#103 Fatal Error: Could Not Calculate " + day_name + " Accurately") # Kill Program, Something Went Very Wrong
        sys.exit("Fatal Error")

    # Run this from Price records which will be updated LIVE 
    # Calculate Live Stock Information *******************************************
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `StockPrices` WHERE `Ticker`=%s AND `Date`=%s" 
        cursor.execute(sql, (ticker, date))
        connection.commit()
        live_data = cursor.fetchall()

    for live in live_data:
        stock_price_live           = live["Price"]
        stock_price_incr           = live["Increase"]
        stock_price_volm           = live["Volume"]
        MAV_Averg                  = live["AvgVolumeNinety"]
        MAL_Averg                  = live["ShortMovingAvg"]
        MAB_Averg                  = live["LongMovingAvg"]
    # Calculate Live Stock Information *******************************************


    # Calculate # of Tweets From Today *******************************************
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `StockTweets` WHERE `Ticker`=%s AND `Date`=%s" 
        cursor.execute(sql, (ticker, date))
        connection.commit()
        today_tweets = cursor.fetchall()
        DailyTweets_Count = cursor.rowcount
    # Calculate # Of Tweets From Today *******************************************
        
        
    # Calculate Sentiment For The Day 
    # *************************************************************************** 
    # SHORT TERM SENTIMENT ANALYSIS 
    # --------------------------------------------       
    # Short Term Sentiment Scale
    #    0   Extremelly Negative Sentiment <-40
    #    0.1                                -40 - -30  
    #    0.2                                -30 - -20
    #    0.3                                -20 - -10
    #    0.4                                -10 - -0    
    #    0.5 Neutral                         0
    #    0.6                                 0  - 10
    #    0.7                                 10 - 20
    #    0.8                                 20 - 30
    #    0.9                                 30 - 40
    #    1   Significant Positive Sentiment    >50
    # --------------------------------------------   
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `StockTweets` WHERE `Ticker`=%s AND `Date`=%s" 
        cursor.execute(sql, (ticker, date))
        connection.commit()
        DaySentiment = cursor.fetchall()            
            
        Daily_Sentiment = 0
        Daily_Count     = 0.001
        for tweet in DaySentiment:
            Temp_Likes     = 0
            Temp_Likes     = float(tweet["Total_Likes"])
            Temp_Sentiment = 0 
            Temp_Sentiment = float(tweet["Tweet_Sentiment"])
            Daily_Count    = Daily_Count + 1

            while(Temp_Likes!=0):
                if((Temp_Sentiment<=90) and (Temp_Sentiment>=-90)): # Prevent Overbounds
                    Temp_Sentiment = (Temp_Sentiment * 0.15) + Temp_Sentiment
                Temp_Likes = Temp_Likes - 1 
            Daily_Sentiment = Daily_Sentiment + Temp_Sentiment    

        SentimentNormalized = (Daily_Sentiment / Daily_Count) # Calculate One Day Sentiment
        SentimentNormalized = round(SentimentNormalized)
    
    if (SentimentNormalized<-40):
        SentimentNormalized = float(0.0) 
    elif((SentimentNormalized>=-40) and (SentimentNormalized<-30)):
        SentimentNormalized = float(0.1) 
    elif((SentimentNormalized>=-30) and (SentimentNormalized<-20)):
        SentimentNormalized = float(0.2) 
    elif((SentimentNormalized>=-20) and (SentimentNormalized<-10)):
        SentimentNormalized = float(0.3) 
    elif((SentimentNormalized>=-10) and (SentimentNormalized<0)):
        SentimentNormalized = float(0.4) 
    elif (SentimentNormalized==0):
        SentimentNormalized = float(0.5) 
    elif((SentimentNormalized>0) and (SentimentNormalized<10)):
        SentimentNormalized = float(0.6)         
    elif((SentimentNormalized>=10) and (SentimentNormalized<20)):
        SentimentNormalized = float(0.7)         
    elif((SentimentNormalized>=20) and (SentimentNormalized<30)):
        SentimentNormalized = float(0.8)                    
    elif((SentimentNormalized>=30) and (SentimentNormalized<=40)):
        SentimentNormalized = float(0.9)    
    elif(SentimentNormalized>40):
        SentimentNormalized = float(1.0) 
    else:
        print("#104 Fatal Error: Could Not Calculate Sentiment Accurately") 
        sys.exit("Fatal Error")
        
    print("Sentiment For " + day_name + "", SentimentNormalized)   
    # Calculate Sentiment For The Day *******************************************
    
    
    # Calculate Prediction Date *************************************************

    start_date        = datetime.strptime(date, '%Y-%m-%d')
    forwardgo         = start_date - timedelta(days=-1)
    forward_date      = forwardgo.strftime('%Y-%m-%d')
    no_weekends       = datetime.strptime((forward_date), '%Y-%m-%d').strftime('%A') # Grab Name of Requested Date
        
    if(no_weekends=="Saturday"):
        start_date        = datetime.strptime(forward_date, '%Y-%m-%d')
        forwardgo         = start_date - timedelta(days=-2)
        forward_date      = forwardgo.strftime('%Y-%m-%d')
        no_weekends       = datetime.strptime((forward_date), '%Y-%m-%d').strftime('%A') # Grab Name of Requested Date
        if((no_weekends=="Saturday") or (no_weekends=="Sunday")):
            print("#105 Fatal Error: Could Not Calculate Date Accurately") # Kill Program, Something Went Very Wrong
            sys.exit("Fatal Error")
    elif(no_weekends=="Sunday"):
        start_date        = datetime.strptime(forward_date, '%Y-%m-%d')
        forwardgo         = start_date - timedelta(days=-1)
        forward_date      = forwardgo.strftime('%Y-%m-%d')
        no_weekends       = datetime.strptime((forward_date), '%Y-%m-%d').strftime('%A') # Grab Name of Requested Date
        if((no_weekends=="Saturday") or (no_weekends=="Sunday")):
            print("#106 Fatal Error: Could Not Calculate Date Accurately") # Kill Program, Something Went Very Wrong
            sys.exit("Fatal Error")
    
    forward_date_id = datetime.strptime((forward_date), '%Y-%m-%d').strftime('%d') 
    
    # Calculate Prediction Date *************************************************

    # Calculate Sentiment + Tweet Volume Average 30 Actual Days * From Date *
    # *************************************************************************** 
    # LONG TERM SENTIMENT ANALYSIS     
    # --------------------------------------------       
    # Calculate and Normalize 30 Day Sentiment Average
    # Long Term Sentiment Scale
    #    0   General Negative Sentiment     <95
    #    0.1                                96
    #    0.2                                97
    #    0.3                                98
    #    0.4                                99
    #    0.5 Average                        100
    #    0.6                                101
    #    0.7                                102
    #    0.8                                103
    #    0.9                                104
    #    1   General Positive Sentiment    >105
    # --------------------------------------------       
   
    days_list = rangedatelist(date, 29)  # Get List of Backdates In This Range (Including Weekends)    
    SAB_Total = 0.0
    SAB_Averg = 0.0
    SAB_Count = 0
    
    TVA_Count = 0       # Daily Tweet Volume  Count
    TVA_Days  = 0.001   # Daily Tweet Volume Total Days
    TVA_Total = 0       # Tweet Volume Average Total
    
    for day in days_list:   # For Each Day In Range, Calculate Sentiment Analysis
        TVA_Days  = TVA_Days + 1
        SAB_Count = SAB_Count + 1
        day = day.strftime('%Y-%m-%d')      
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `StockTweets` WHERE `Ticker`=%s AND `Date`=%s" 
            cursor.execute(sql, (ticker, day))
            connection.commit()
            one_day = cursor.fetchall()
            
        Daily_Sentiment = 0
        Daily_Count     = 0.001
        for tweet in one_day:
            TVA_Count      = TVA_Count + 1 
            Temp_Likes     = 0
            Temp_Likes     = float(tweet["Total_Likes"])
            Temp_Sentiment = 0 
            Temp_Sentiment = float(tweet["Tweet_Sentiment"])
            Daily_Count    = Daily_Count + 1

            while(Temp_Likes!=0):
                if((Temp_Sentiment<=90) and (Temp_Sentiment>=-90)): # Prevent Overbounds
                    Temp_Sentiment = (Temp_Sentiment * 0.15) + Temp_Sentiment
                Temp_Likes = Temp_Likes - 1 
            Daily_Sentiment = Daily_Sentiment + Temp_Sentiment    
        if(Daily_Sentiment==0):
            TVA_Days = TVA_Days - 1 # Fix Averages If No Tweets On That Day
             
        Tweet_Sentiment = (Daily_Sentiment / Daily_Count) # Calculate One Day Sentiment
        SAB_Total = SAB_Total + Tweet_Sentiment  # Add One Day Sentiment To SAB Total
    TVA_Total = (TVA_Count / TVA_Days)
    SAB_Averg = (SAB_Total / SAB_Count) 
    SAB_Averg = round(SAB_Averg)
    SAB_Averg = SAB_Averg + 100
    print("30 Day Sentiment", SAB_Averg)      
    print("30 Day Avg Tweets", TVA_Total)    
    
    if (SAB_Averg<=95):
        SentimentLongTerm = float(0.0) 
    elif(SAB_Averg==96):
        SentimentLongTerm = float(0.1) 
    elif(SAB_Averg==97):
        SentimentLongTerm = float(0.2) 
    elif(SAB_Averg==98):
        SentimentLongTerm = float(0.3) 
    elif(SAB_Averg==99):
        SentimentLongTerm = float(0.4) 
    elif(SAB_Averg==100):
        SentimentLongTerm = float(0.5) 
    elif(SAB_Averg==101):
        SentimentLongTerm = float(0.6) 
    elif(SAB_Averg==102):
        SentimentLongTerm = float(0.7) 
    elif(SAB_Averg==103):
        SentimentLongTerm = float(0.8) 
    elif(SAB_Averg==104):
        SentimentLongTerm = float(0.9) 
    elif(SAB_Averg>=105):
        SentimentLongTerm = float(1.0) 
    else:
        print("#201 Fatal Error: Could Not Calculate Sentiment Accurately") 
        sys.exit("Fatal Error")    
    # Calculate Sentiment + Volume Average 30 Actual Days * From Date *
    # *************************************************************************** 


    # TRADING VOLUME ANALYSIS    
    # *************************************************************************** 
    # --------------------------------------------       
    # Calculate and Normalize Volume Trading
    # Trading Volume Scale
    #    0   Unusually Low Volume       0,1
    #    0.1                            2,3
    #    0.2                            4,5
    #    0.3                            6,7
    #    0.4                            8,9
    #    0.5 Average                    10
    #    0.6                            11,12
    #    0.7                            13,14
    #    0.8                            15,16
    #    0.9                            17,18
    #    1   Unusually High Volume      19,20
    # --------------------------------------------       
   
    ThisDay_Volume = int(stock_price_volm)
    MAV_Averg      = int(MAV_Averg)  # Pulled From LiveDatabase
    if(ThisDay_Volume>MAV_Averg):
        Sub_Process = (ThisDay_Volume / MAV_Averg)
        Sub_Process = 10 * Sub_Process
        VolumeNormalized = Sub_Process
        if(Sub_Process>20):    # Maximum Volume Increase Is Double
            Sub_Process = 20 
            VolumeNormalized = Sub_Process
        elif(Sub_Process<10):   # This shouldn't ever happen
            Sub_Process = 10
            VolumeNormalized = Sub_Process
    elif(ThisDay_Volume<MAV_Averg):
        Sub_Process = (ThisDay_Volume / MAV_Averg)
        Sub_Process = 10 * Sub_Process
        VolumeNormalized = Sub_Process 
        if(Sub_Process<0):    # No Negatives Allowed
            Sub_Process = 0 
            VolumeNormalized = Sub_Process
        elif(Sub_Process>10):  # This shouldn't ever happen
            Sub_Process = 10
            VolumeNormalized = Sub_Process
    else:
        VolumeNormalized = 10
    VolumeNormalized = round(VolumeNormalized)
    if((VolumeNormalized==0) or (VolumeNormalized==1)):
        VolumeNormalized = float(0.0)
    elif((VolumeNormalized==2) or (VolumeNormalized==3)):
        VolumeNormalized = float(0.1)
    elif((VolumeNormalized==4) or (VolumeNormalized==5)):
        VolumeNormalized = float(0.2)
    elif((VolumeNormalized==6) or (VolumeNormalized==7)):
        VolumeNormalized = float(0.3)
    elif((VolumeNormalized==8) or (VolumeNormalized==9)):
        VolumeNormalized = float(0.4)
    elif(VolumeNormalized==10):
        VolumeNormalized = float(0.5)
    elif((VolumeNormalized==11) or (VolumeNormalized==12)):
        VolumeNormalized = float(0.6)
    elif((VolumeNormalized==13) or (VolumeNormalized==14)):
        VolumeNormalized = float(0.7)
    elif((VolumeNormalized==15) or (VolumeNormalized==16)):
        VolumeNormalized = float(0.8)
    elif((VolumeNormalized==17) or (VolumeNormalized==18)):
        VolumeNormalized = float(0.9)
    elif((VolumeNormalized==19) or (VolumeNormalized==20)):
        VolumeNormalized = float(1.0)
    else:
        print("#202 Fatal Error: Could Not Calculate Volume Accurately") 
        sys.exit("Fatal Error")
    # *************************************************************************** 

        
    # Calculate and Normalize Daily Sentiment
    # *************************************************************************** 
    # SHORT TERM TWEET VOLUME     
    # --------------------------------------------       
    # Calculate and Normalize Tweet Volume
    # Tweet Volume Scale
    #    0   Unusually Low Volume       0,1
    #    0.1                            2,3
    #    0.2                            4,5
    #    0.3                            6,7
    #    0.4                            8,9
    #    0.5 Average                    10
    #    0.6                            11,12
    #    0.7                            13,14
    #    0.8                            15,16
    #    0.9                            17,18
    #    1   Unusually High Volume      19,20
    # --------------------------------------------       

    DailyTweets_Count = int(DailyTweets_Count)
    TVA_Total         = int(TVA_Total)
    if(DailyTweets_Count>MAV_Averg):
        Sub_Process = (DailyTweets_Count / TVA_Total)
        Sub_Process = 10 * Sub_Process
        TweetsNormalized = Sub_Process
        if(Sub_Process>20):    # Maximum Volume Increase Is Double
            Sub_Process = 20 
            TweetsNormalized = Sub_Process
        elif(Sub_Process<10):   # This shouldn't ever happen
            Sub_Process = 10
            TweetsNormalized = Sub_Process
    elif(DailyTweets_Count<TVA_Total):
        Sub_Process = (DailyTweets_Count / TVA_Total)
        Sub_Process = 10 * Sub_Process
        TweetsNormalized = Sub_Process 
        if(Sub_Process<0):    # No Negatives Allowed
            Sub_Process = 0 
            TweetsNormalized = Sub_Process
        elif(Sub_Process>10):  # This shouldn't ever happen
            Sub_Process = 10
            TweetsNormalized = Sub_Process
    else:
        TweetsNormalized = 10
    TweetsNormalized = round(TweetsNormalized)
    if((TweetsNormalized==0) or (TweetsNormalized==1)):
        TweetsNormalized = float(0.0) 
    elif((TweetsNormalized==2) or (TweetsNormalized==3)):
        TweetsNormalized = float(0.1) 
    elif((TweetsNormalized==4) or (TweetsNormalized==5)):
        TweetsNormalized = float(0.2) 
    elif((TweetsNormalized==6) or (TweetsNormalized==7)):
        TweetsNormalized = float(0.3) 
    elif((TweetsNormalized==8) or (TweetsNormalized==9)):
        TweetsNormalized = float(0.4) 
    elif(TweetsNormalized==10):
        TweetsNormalized = float(0.5) 
    elif((TweetsNormalized==11) or (TweetsNormalized==12)):
        TweetsNormalized = float(0.6) 
    elif((TweetsNormalized==13) or (TweetsNormalized==14)):
        TweetsNormalized = float(0.7) 
    elif((TweetsNormalized==15) or (TweetsNormalized==16)):
        TweetsNormalized = float(0.8) 
    elif((TweetsNormalized==17) or (TweetsNormalized==18)):
        TweetsNormalized = float(0.9) 
    elif((TweetsNormalized==19) or (TweetsNormalized==20)):
        TweetsNormalized = float(1.0) 
    else:
        print("#203 Fatal Error: Could Not Calculate Volume Accurately") 
        sys.exit("Fatal Error")

    # Calculate and Normalize Volume Trading
    # ***************************************************************************     


    # ***************************************************************************     
    # Check Above or Below Moving Averages
  
    if(stock_price_live > MAB_Averg):
        AboveBigMoving = 1
    else:
        AboveBigMoving = 0
        
    if(stock_price_live < MAL_Averg):
        BelowLittleMoving = 1
    else:
        BelowLittleMoving = 0
    # Check Above or Below Moving Averages
    # ***************************************************************************     

    # Algorithm Results
    # ***************************************************************************
    print("\n\n")
    print("Neural Network Normalized Data: ")
    print("----------------------------------------------")
    print("Entry                                  ", Entry)
    print("Volume Normalized:    [0,1]            ", VolumeNormalized)
    print("Tweets Normalized:    [0,1]            ", TweetsNormalized)
    print("Sentiment Analysis:   [0,1]            ", SentimentNormalized)
    print("Above Big Moving:     [0,1]            ", AboveBigMoving)
    print("Below Little Moving:  [0,1]            ", BelowLittleMoving)
    print("Trading Day:          [0,1]            ", trading_day)
    print("Trading Season:       [Sp, Su, Fa, Wi] ", trading_season)    
    print("Moving Avg Sentiment: [0,200]          ", SAB_Averg)

    outputs = network.process([
            trading_day,          trading_season, 
            VolumeNormalized,     AboveBigMoving,
            BelowLittleMoving,    VolumeNormalized, 
            SentimentNormalized,  SentimentLongTerm
    ])
    
    result1 = round(outputs[0], 2)
    result2 = round(outputs[1], 2)

    print("Results")
    print("--------------------------------------------------")
    print("Prediction:       [", result1, ",", result2, "]")
    print("\n")
    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Predictions` WHERE `PredictionDate`=%s AND Ticker=%s"
            cursor.execute(sql, (forward_date, ticker))
            result = cursor.fetchone()
        
        if result is None:
            print("Success: Inserting Prediction To Records:      ", ticker)
            with connection.cursor() as cursor:
                sql = "INSERT INTO `Predictions` (`Date`, `PredictionDate`, `Day_ID`, `PredictionDateName`, `Ticker`, `InitialPrice`, `Entry`, `Pred_Output1`, `Pred_Output2`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (Today, forward_date, forward_date_id, no_weekends, ticker, stock_price_live, Entry, result1, result2))
                connection.commit()
        else:
            print("Success: Updating Prediction In Records:      ", ticker)
            unique_entry = result["Entry"]
            
            cursor = connection.cursor()
            sql = "UPDATE Predictions SET Date=%s WHERE Entry=%s"
            cursor.execute(sql, (Today, unique_entry))
            connection.commit()
            
            cursor = connection.cursor()
            sql = "UPDATE Predictions SET InitialPrice=%s WHERE Entry=%s"
            cursor.execute(sql, (stock_price_live, unique_entry))
            connection.commit()

            cursor = connection.cursor()
            sql = "UPDATE Predictions SET PredictionDate=%s WHERE Entry=%s"
            cursor.execute(sql, (forward_date, unique_entry))
            connection.commit()
            
            cursor = connection.cursor()
            sql = "UPDATE Predictions SET PredictionDateName=%s WHERE Entry=%s"
            cursor.execute(sql, (no_weekends, unique_entry))
            connection.commit()
            
            cursor = connection.cursor()
            sql = "UPDATE Predictions SET Pred_Output1=%s WHERE Entry=%s"
            cursor.execute(sql, (result1, unique_entry))
            connection.commit()
        
            cursor = connection.cursor()
            sql = "UPDATE Predictions SET Pred_Output2=%s WHERE Entry=%s"
            cursor.execute(sql, (result2, unique_entry))
            connection.commit()
            
            cursor = connection.cursor()
            sql = "UPDATE Predictions SET Day_ID=%s WHERE Entry=%s"
            cursor.execute(sql, (forward_date_id, unique_entry))
            connection.commit()
        
    finally:
        # Adjusted for possibility that network is not fully trained yet.
        # Fine tune this as time goes forward
    
        if((result1>=0.0) and (result1<=0.15)):
            approx = 0.0
        elif((result1>0.15) and (result1<0.45)):
            approx = 0.3
        elif((result1>=0.45) and (result1<0.55)):
            approx = -1.0          
        elif((result1>=0.55) and (result1<0.85)):
            approx = 0.7
        elif((result1>=0.85) and (result1<=1.00)):
            approx = 1.0

        if(approx==0.0):
            prediction_event = "Significant Decrease"
        elif(approx==0.3):
            prediction_event = "Decrease" 
        elif(approx==0.7):  
            prediction_event = "Increase"
        elif(approx==1.0):
            prediction_event = "Significant Increase"
        elif(approx==-1.0):
            prediction_event = "Inconclusive"
            
        confidence = 0
        boost      = 0.0

        if(AboveBigMoving==1):
            boost = boost + 0.13
        if(BelowLittleMoving==1):
            boost = boost + 0.13        
            
        if(approx == 0.0):
            if(result1==0.0):
                confidence = 10
            if(result1==0.01):  
                confidence = 9
            if(result1==0.02):   
                confidence = 9
            if(result1==0.03):  
                confidence = 9
            if(result1==0.04): 
                confidence = 8
            if(result1==0.05):    
                confidence = 8
            if(result1==0.06):
                confidence = 7
            if(result1==0.07):       
                confidence = 7
            if(result1==0.08):     
                confidence = 6
            if(result1==0.09): 
                confidence = 6
            if(result1==0.10):   
                confidence = 6
            if(result1==0.11):
                confidence = 6
            if(result1==0.12):
                confidence = 6
            if(result1==0.13):
                confidence = 6
            if(result1==0.14):
                confidence = 6
            if(result1==0.15):
                confidence = 6
        if(approx == 0.3):
            if(result1==0.16):
                confidence = 5
            if(result1==0.17):  
                confidence = 5
            if(result1==0.18):   
                confidence = 5
            if(result1==0.19):  
                confidence = 5
            if(result1==0.20): 
                confidence = 5
            if(result1==0.21):    
                confidence = 5
            if(result1==0.22):
                confidence = 6
            if(result1==0.23):       
                confidence = 6
            if(result1==0.24):     
                confidence = 7
            if(result1==0.25): 
                confidence = 7
            if(result1==0.26):   
                confidence = 7
            if(result1==0.27):
                confidence = 8
            if(result1==0.28):
                confidence = 8
            if(result1==0.29):
                confidence = 9
            if(result1==0.30):
                confidence = 9
            if(result1==0.31):  
                confidence = 9
            if(result1==0.32):   
                confidence = 8
            if(result1==0.33):  
                confidence = 7
            if(result1==0.34): 
                confidence = 6
            if(result1==0.35):    
                confidence = 6
            if(result1==0.36):
                confidence = 5
            if(result1==0.37):       
                confidence = 5
            if(result1==0.38):     
                confidence = 4
            if(result1==0.39): 
                confidence = 3
            if(result1==0.40):   
                confidence = 3
            if(result1==0.41):
                confidence = 2
            if(result1==0.42):
                confidence = 2
            if(result1==0.43):
                confidence = 1
            if(result1==0.44):
                confidence = 1
        if(approx == -1.0):
            if(result1==0.45):
                confidence = 0
            if(result1==0.46):  
                confidence = 0
            if(result1==0.47):   
                confidence = 0
            if(result1==0.48):  
                confidence = 0
            if(result1==0.49): 
                confidence = 0
            if(result1==0.50):    
                confidence = 0
            if(result1==0.51):
                confidence = 0
            if(result1==0.52):       
                confidence = 0
            if(result1==0.53):     
                confidence = 0
            if(result1==0.54): 
                confidence = 0
        if(approx == 0.7):
            if(result1==0.55):
                confidence = 1
            if(result1==0.56):  
                confidence = 1
            if(result1==0.57):   
                confidence = 2
            if(result1==0.58):  
                confidence = 2
            if(result1==0.59): 
                confidence = 2
            if(result1==0.60):    
                confidence = 3
            if(result1==0.61):
                confidence = 3
            if(result1==0.62):       
                confidence = 4
            if(result1==0.63):     
                confidence = 5
            if(result1==0.64): 
                confidence = 5
            if(result1==0.65):   
                confidence = 6
            if(result1==0.66):
                confidence = 7
            if(result1==0.67):
                confidence = 8
            if(result1==0.68):
                confidence = 8
            if(result1==0.69):
                confidence = 9
            if(result1==0.70):  
                confidence = 9
            if(result1==0.71):   
                confidence = 9
            if(result1==0.72):  
                confidence = 8
            if(result1==0.73): 
                confidence = 8
            if(result1==0.74):    
                confidence = 7
            if(result1==0.75):
                confidence = 7
            if(result1==0.76):       
                confidence = 6
            if(result1==0.77):     
                confidence = 6
            if(result1==0.78): 
                confidence = 6
            if(result1==0.79):   
                confidence = 5
            if(result1==0.80):
                confidence = 5
            if(result1==0.81):
                confidence = 5
            if(result1==0.82):
                confidence = 5
            if(result1==0.83):
                confidence = 5
            if(result1==0.84):
                confidence = 5
        if(approx == 1.0):
            if(result1==0.85):
                confidence = 5
            if(result1==0.86):  
                confidence = 5
            if(result1==0.87):   
                confidence = 5
            if(result1==0.88):  
                confidence = 5
            if(result1==0.89): 
                confidence = 5
            if(result1==0.90):    
                confidence = 5
            if(result1==0.91):
                confidence = 6
            if(result1==0.92):       
                confidence = 6
            if(result1==0.93):     
                confidence = 6
            if(result1==0.94): 
                confidence = 6
            if(result1==0.95):   
                confidence = 7
            if(result1==0.96):
                confidence = 8
            if(result1==0.97):
                confidence = 9
            if(result1==0.98):
                confidence = 9
            if(result1==0.99):
                confidence = 9
            if(result1==1.00):
                confidence = 9       
                
        confidence = (confidence + (confidence * boost))
        
        cursor = connection.cursor()
        sql = "UPDATE Stocks SET Prediction=%s WHERE Ticker=%s"
        cursor.execute(sql, (prediction_event, ticker))
        connection.commit()

        cursor = connection.cursor()
        sql = "UPDATE Stocks SET Prediction_Day=%s WHERE Ticker=%s"
        cursor.execute(sql, (no_weekends, ticker))
        connection.commit()

        cursor = connection.cursor()
        sql = "UPDATE Stocks SET Confidence=%s WHERE Ticker=%s"
        cursor.execute(sql, (confidence, ticker))
        connection.commit()

        cursor = connection.cursor()
        sql = "UPDATE Predictions SET Confidence=%s WHERE PredictionDate=%s AND Ticker=%s"
        cursor.execute(sql, (confidence, forward_date, ticker))
        connection.commit()

        cursor = connection.cursor()
        sql = "UPDATE Predictions SET Prediction=%s WHERE PredictionDate=%s AND Ticker=%s"
        cursor.execute(sql, (prediction_event, forward_date, ticker))
        connection.commit()
                    
        print("::: SAVING DATA ::: DO NOT CLOSE CONNECTION :::")
    
def main():
    connect = connection.connection()
    ticker_list = []
    
    with connect.cursor() as cursor:
        sql = "SELECT * FROM `Stocks` WHERE `Status`='Active' ORDER BY RAND() LIMIT 100" 
        cursor.execute(sql, ())
        connect.commit()
        active = cursor.fetchall()
        
    for stock in active:
        ticker = stock["Ticker"].rstrip()
        ticker_list.append(ticker)
    
    for stock in active:
        backtrack  = datetime.today() - timedelta(days=0)
        prediction_on_date = backtrack.strftime('%Y-%m-%d')        
    
        ticker_sybmbol = stock["Ticker"].rstrip()
        ticker_company = stock["Company"].rstrip()
        
        print("Neural Predictions------------------------------------------")
        print(ticker_company, "for date", prediction_on_date)
        neuralcalculations(connect, ticker_sybmbol, prediction_on_date)        
        
    connect.close()
    print("*********** Program Completed ***********")    
    
if __name__ == "__main__":
    main()