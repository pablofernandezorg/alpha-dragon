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
import update
import pulldata

from datetime import date, datetime, timedelta
import random
import sys

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
    date_parts = date.split("-") # Explode Date
    year       = date_parts[0]   # Grab The Date
    month      = date_parts[1]   # Grab The Date
    day        = date_parts[2]   # Grab The Date
    Today                        = datetime.today().strftime('%Y-%m-%d') # Grab Todays Date
    Entry                        = random.randint(2000000000,60000000000) 
    DayOfWeek                    = day     # Day of Week
    TickerSymbol                 = ticker  #Ticker Symbol 
    
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
        print("Fatal Error: Invalid Date Input Received") # Kill Program, Request Not Allowed
        sys.exit("Fatal Error")
            
    if((month=="3") or (month=="4") or (month=="5")):
        trading_season = 0.25
    elif((month=="6") or (month=="7") or (month=="8")):
        trading_season = 0.50
    elif((month=="9") or (month=="10") or (month=="11")):
        trading_season = 0.75
    elif((month=="12") or (month=="1") or (month=="2")):
        trading_season = 1.0
    else:
        print("Fatal Error: Could Not Calculate " + day_name + " Accurately") # Kill Program, Something Went Very Wrong
        sys.exit("Fatal Error")


# Calculate Moving Average 200 Trading Days * From Date *
# *************************************************************************** 
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `StockPrices` WHERE `Ticker`=%s ORDER BY Date DESC" 
        cursor.execute(sql, (ticker))
        connection.commit()
        MovingAvgBig = cursor.fetchall()

    days_list = rangedatelist(date, 286)  # Get List of Backdates In This Range (Including Weekends) 
                        
    MAB_Total = 0.0
    MAB_Averg = 0.0
    MAB_Count = 0

    for day in MovingAvgBig:
        MAB_Closing = day['Closing_Price']
        MAB_Date    = day['Date']
        MAB_Date    = datetime.strptime(MAB_Date, '%Y-%m-%d') # Convert to Datetime
    
        if ((MAB_Date in days_list) and (MAB_Count<200)): 
            MAB_Count = MAB_Count + 1
            MAB_Total   = MAB_Total + float(MAB_Closing)
                    
    print("Counter Check: ", MAB_Count)
    MAB_Averg = (MAB_Total / MAB_Count)
    MAB_Averg = round(MAB_Averg, 2)
    print("200 Day Moving Average: ", MAB_Averg)
    update.large_moving_avg(connection, MAB_Averg, ticker)
    
# Calculate Moving Average 200 Trading Days * From Date *
# *************************************************************************** 
   
# Calculate Moving Average 5 Trading Days * From Date *
# *************************************************************************** 
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `StockPrices` WHERE `Ticker`=%s ORDER BY Date DESC" 
        cursor.execute(sql, (ticker))
        connection.commit()
        MovingAvgLittle = cursor.fetchall()
        
    drop_today     = datetime.strptime(date, '%Y-%m-%d')
    back_today     = drop_today - timedelta(days=1)
    back_today     = back_today.strftime('%Y-%m-%d')    
    days_list = rangedatelist(back_today, 7)  # Get List of Backdates In This Range (Including Weekends)  
        
    MAL_Total = 0.0
    MAL_Averg = 0.0
    MAL_Count = 0

    for day in MovingAvgLittle:
        MAL_Closing = day['Closing_Price'] 
        MAL_Date    = day['Date']
        MAL_Date    = datetime.strptime(MAL_Date, '%Y-%m-%d') # Convert to Datetime

        if ((MAL_Date in days_list) and (MAL_Count<5)):
            MAL_Count = MAL_Count + 1
            MAL_Total   = MAL_Total + float(MAL_Closing)
            
    print("Counter Check: ", MAL_Count)
    MAL_Averg = (MAL_Total / MAL_Count) 
    MAL_Averg = round(MAL_Averg, 2)
    print("5 Day Moving Average: ", MAL_Averg)  
    update.small_moving_avg(connection, MAL_Averg, ticker)
    
# Calculate Moving Average 5 Trading Days * From Date *
# *************************************************************************** 
    
    
    
    
# Calculate Volume Average 90 Trading Days * From Date *
# *************************************************************************** 
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `StockPrices` WHERE `Ticker`=%s ORDER BY Date DESC" 
        cursor.execute(sql, (ticker))
        connection.commit()
        MovingAvgVolume = cursor.fetchall()
        
    days_list = rangedatelist(date, 130)  # Get List of Backdates In This Range (Including Weekends)    
        
    MAV_Total = 0.0
    MAV_Averg = 0.0
    MAV_Count = 0

    for day in MovingAvgVolume:
        MAV_Volume = day['Volume']
        MAV_Date   = day['Date']
        MAV_Date    = datetime.strptime(MAV_Date, '%Y-%m-%d') # Convert to Datetime
        
        if ((MAV_Date in days_list) and (MAV_Count<90)) : 
            MAV_Count = MAV_Count + 1
            MAV_Total   = MAV_Total + float(MAV_Volume)
            
    print("Counter Check: ", MAV_Count)
    MAV_Averg = (MAV_Total / MAV_Count) 
    MAV_Averg = round(MAV_Averg)
    print("Average Volume 90 Days: ", MAV_Averg)
    update.avg_volume_long(connection, MAV_Averg, ticker)
    
# Calculate Volume Average 90 Trading Days * From Date *
# *************************************************************************** 
 
# Calculate # of Tweets From Today *******************************************
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `StockTweets` WHERE `Ticker`=%s AND `Date`=%s" 
        cursor.execute(sql, (ticker, date))
        connection.commit()
        today_tweets = cursor.fetchall()
        DailyTweets_Count = cursor.rowcount
        update.today_tweets(connection, DailyTweets_Count, ticker)
        
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
        print("Fatal Error: Could Not Calculate Sentiment Accurately") 
        sys.exit("Fatal Error")
        
    print("Sentiment For " + day_name + "", SentimentNormalized)   
# Calculate Sentiment For The Day *******************************************
    


# Calculate Sentiment + Volume Average 30 Actual Days * From Date *
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
    update.avg_sentiment_short(connection, SAB_Averg, ticker)

    print("30 Day Avg Tweets", TVA_Total)    
    update.avg_tweets_short(connection, TVA_Total, ticker)
    
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
        print("Fatal Error: Could Not Calculate Sentiment Accurately") 
        sys.exit("Fatal Error")    
# Calculate Sentiment + Volume Average 30 Actual Days * From Date *
# *************************************************************************** 


# Grab Pricing For Two Trading Days Requested and Following
# *************************************************************************** 
    if((day_name=="Saturday") or (day_name=="Sunday")):
        print("Error: You cannot request a neural programming for a weekend")
    else:
        safety_check = 0
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `StockPrices` WHERE `Ticker`=%s AND `Date`=%s" 
            cursor.execute(sql, (ticker, date))
            connection.commit()
            prices_on_date = cursor.fetchall()
            safety_check = cursor.rowcount
            
        if(safety_check == 0):
            print("Error: No Date Record Exists For The Date Requested")
            sys.exit("Fatal Error") # Kill Program, Bad User Input
        else:
            for pricing in prices_on_date:
                ThisDay_Volume  = pricing["Volume"]
                ThisDay_Closing = pricing["Closing_Price"]
                ThisDay_HighPr  = pricing["High_Price"]
                ThisDay_LowPr   = pricing["Low_Price"]
    
                print("Lookup Volume:       ", ThisDay_Volume)
                print("Lookup High:         ", ThisDay_HighPr)
                print("Lookup Low:          ", ThisDay_LowPr)
                print("Lookup Close:        ", ThisDay_Closing)

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
                print("Fatal Error: Could Not Calculate Date Accurately") # Kill Program, Something Went Very Wrong
                sys.exit("Fatal Error")
        elif(no_weekends=="Sunday"):
            start_date        = datetime.strptime(forward_date, '%Y-%m-%d')
            forwardgo         = start_date - timedelta(days=-1)
            forward_date      = forwardgo.strftime('%Y-%m-%d')
            no_weekends       = datetime.strptime((forward_date), '%Y-%m-%d').strftime('%A') # Grab Name of Requested Date
            if((no_weekends=="Saturday") or (no_weekends=="Sunday")):
                print("Fatal Error: Could Not Calculate Date Accurately") # Kill Program, Something Went Very Wrong
                sys.exit("Fatal Error")      
      
        print("Next Day: ", no_weekends)
        print("Next Day: ", forward_date)

        with connection.cursor() as cursor:
            sql = "SELECT * FROM `StockPrices` WHERE `Ticker`=%s AND `Date`=%s" 
            cursor.execute(sql, (ticker, forward_date))
            connection.commit()
            prices_on_forward_date = cursor.fetchall()
            safety_check = cursor.rowcount

        NextDay_Volume   = 0.01
        NextDay_HighPr   = 0.01
        NextDay_LowPr    = 0.01
        NextDay_Closing  = 0.01
        
        for pricing in prices_on_forward_date:
            NextDay_Volume  = pricing["Volume"]
            NextDay_Closing = pricing["Closing_Price"]
            NextDay_HighPr  = pricing["High_Price"]
            NextDay_LowPr   = pricing["Low_Price"]

        if(NextDay_Closing==0.01):
            print("Fatal Error: Forward Date Price Data Not Available") 
            sys.exit("Fatal Error")
    
        print("Next Day------------------------------")
        print("Lookup Volume:      ", NextDay_Volume)
        print("Lookup High:        ", NextDay_HighPr)
        print("Lookup Low:         ", NextDay_LowPr)
        print("Lookup Close:       ", NextDay_Closing)
# Grab Pricing For Two Trading Days Requested and Following
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
   
    ThisDay_Volume = int(ThisDay_Volume)
    MAV_Averg      = int(MAV_Averg)
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
        print("Fatal Error: Could Not Calculate Volume Accurately") 
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
        print("Fatal Error: Could Not Calculate Volume Accurately") 
        sys.exit("Fatal Error")

# Calculate and Normalize Volume Trading
# ***************************************************************************     

# Calculate Results From The Next Day
# ***************************************************************************  
#  0.0   Stock price decreased 
#  0.2   Stock price decreased by <1%
#  0.3
#  0.4
#  ———————————————————
#  0.4
#  0.5
#  0.6   Stock price increased by <1%
#  1.0 Stock price increased        

    ThisDay_Closing = float(ThisDay_Closing)
    NextDay_Closing = float(NextDay_Closing)
    
    if(ThisDay_Closing<=NextDay_Closing):             # Stock price increased
        change_percent = (((NextDay_Closing - ThisDay_Closing)/ThisDay_Closing)*100)
        if(change_percent>1.0):
            Output1   =  1.0
            Output2   =  1.0
        else:
            Output1   =  0.7
            Output2   =  0.7
    if(ThisDay_Closing>NextDay_Closing):              # Stock price decreased
        change_percent = (((ThisDay_Closing - NextDay_Closing)/ThisDay_Closing)*100)
        if(change_percent>1.0):
            Output1   =  0.0
            Output2   =  0.0
        else:
            Output1   =  0.3
            Output2   =  0.3    
        
    if(ThisDay_Closing<=NextDay_Closing):             # Stock price increased
        change_percent = (((NextDay_Closing - ThisDay_Closing)/ThisDay_Closing)*100)
        if(change_percent>2.0):
            Output3   =  1.0
            Output4   =  1.0
        else:
            Output3   =  0.7
            Output4   =  0.7
    if(ThisDay_Closing>NextDay_Closing):              # Stock price decreased
        change_percent = (((ThisDay_Closing - NextDay_Closing)/ThisDay_Closing)*100)
        if(change_percent>2.0):
            Output3   =  0.0
            Output4   =  0.0
        else:
            Output3   =  0.3
            Output4   =  0.3    
        
    if(ThisDay_Closing<=NextDay_Closing):             # Stock price increased
        Output5   =  1.0
        Output6   =  1.0    
       
    if(ThisDay_Closing>NextDay_Closing):              # Stock price decreased
        Output5   =  0.0
        Output6   =  0.0    
               
        
    if(ThisDay_Closing > MAB_Averg):
        AboveBigMoving = 1
    else:
        AboveBigMoving = 0
        
    if(ThisDay_Closing < MAL_Averg):
        BelowLittleMoving = 1
    else:
        BelowLittleMoving = 0
        
# Calculate Results From The Next Day
# ***************************************************************************     


# Algorithm Results
# ***************************************************************************
    print("\n\n")
    print("Neural Network Normalized Data: ")
    print("----------------------------------------------")
    print("Entry                                  ", Entry)
    print("Volume Normalized:    [0,20]           ", VolumeNormalized)
    print("Tweets Normalized:    [0,20]           ", TweetsNormalized)
    print("Sentiment Analysis:   [0,200]          ", SentimentNormalized)
    print("Above Big Moving:     [0,1]            ", AboveBigMoving)
    print("Below Little Moving:  [0,1]            ", BelowLittleMoving)
    print("Trading Day:          [1,5]            ", trading_day)
    print("Trading Season:       [Sp, Su, Fa, Wi] ", trading_season)
    
    print("Moving Avg Sentiment: [0,200]  ", SAB_Averg)

    print("Results:   [",Output1,",",Output2,"]"," Up1%/Up/Down/Down1%")
    print("Results:   [",Output3,",",Output4,"]"," Up2%/Up/Down/Down2%")
    print("Results:   [",Output5,",",Output6,"]"," Up/Down")

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `NeuralNetwork` WHERE `Date`=%s AND Ticker=%s"
            cursor.execute(sql, (date,ticker))
            result = cursor.fetchone()
            
        if result is None:
            print("Success: Inserting Neural Data Set:      ", ticker)
            with connection.cursor() as cursor:
                sql = "INSERT INTO `NeuralNetwork` (`Date`, `Entry`, `TradingDay`, `TradingSeason`, `VolumeNormalized`, `AboveBigMoving`, `BelowLittleMoving`, `TweetsVolumeNormalized`, `Sentiment`, `Ticker`, `Output1`, `Output2`, `Output3`, `Output4`, `Output5`, `Output6`, `Sentiment30`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (date, Entry, trading_day, trading_season, VolumeNormalized, AboveBigMoving, BelowLittleMoving, TweetsNormalized, SentimentNormalized, ticker, Output1, Output2, Output3, Output4, Output5, Output6, SentimentLongTerm))
                connection.commit()
            update.last_input(connection, ticker)
        else:
            print("Error: Neural Data Set Exists For The Date ", ticker, date)
    
    finally:
        print("::: SAVING DATA ::: DO NOT CLOSE CONNECTION :::")
        #connection.close()
    
def main():
    connect = connection.connection()
    
    ticker_list = []
    active      = pulldata.pull_active_stocks(connect)
    
    for stock in active:
        ticker = stock["Ticker"].rstrip()
        ticker_list.append(ticker)
    
    for stock in active:
        backtrack  = datetime.today() - timedelta(days=2)
        send_date = backtrack.strftime('%Y-%m-%d')        
            
        ticker_sybmbol = stock["Ticker"].rstrip()
        ticker_company = stock["Company"].rstrip()
        print("Current calculating: ", ticker_company, "for date", send_date)
        neuralcalculations(connect, ticker_sybmbol, send_date)        
        
    connect.close()
    print("*********** Program Completed ***********")    
    
if __name__ == "__main__":
    main()
