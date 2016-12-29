Alpha Dragon AI&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://openclipart.org/image/2400px/svg_to_png/222990/Tribal-Dragon-26.png" height="40">
========
ww<i></i>w.<i></i>alphadragon.net

Version 5.0. Developed by Pablo Fernandez. Copyright 2016. 

Alpa Dragon is an AI software program that analyses investor sentiment across the internet to create actionable predictions in the stock market. The algorithm runs language analysis on the data and combines this with proven technical indicators to train several neural networks. 

Due to the proprietary nature of this program, several algorithms have been witheld from Github. 

Module Distribution
-----------
```
    main.py          #    Main file used to import, analyze, and store information
    modify.py        #    Parsing twitter information
    fetchdata.py     #    Fetch data from Twitter & Yahoo finance 
    pulldata.py      #    Pull any sort of information from the database
    insertdata.py    #    Insert tweets & stock prices into database    
    analysis.py      #    Scoring API for language analysis
    update.py        #    Push any sort Of update to the database
    connection.py    #    Confidential Server Database Authentication & Connection
    networktrain.py  #    Runs all the calculations needed for the neural network
    
    /neuralnetwork/
    neuralnetwork.py #    Creates the Neural Network and trains it with the database
    
```

Price Movement
-----------
```
    [0.0, 0.0]    Stock price decreased
    [0.5, 0.5]    Stock price changed less than 1%
    [1.0, 1.0]    Stock price increased
```


Long Term Sentiment Scale (30 Day Moving Average)
-----------
```
    0   General Negative Sentiment     <95
    0.1                                96
    0.2                                97
    0.3                                98
    0.4                                99
    0.5 Average                        100
    0.6                                101
    0.7                                102
    0.8                                103
    0.9                                104
    1   General Positive Sentiment    >105
```


Short Term Sentiment Scale (1 Day Average)
-----------
```
    0   Extremelly Negative Sentiment  <-40
    0.1                                 -40 - -30  
    0.2                                 -30 - -20
    0.3                                 -20 - -10
    0.4                                 -10 - -0 
    0.5 Neutral                          0
    0.6                                  0  - 10
    0.7                                  10 - 20
    0.8                                  20 - 30
    0.9                                  30 - 40
    1   Significant Positive Sentiment  >50
```

Share Trading Volume Discrepancies
-----------
```
    0   Unusually Low Volume       0,1
    0.1                            2,3
    0.2                            4,5
    0.3                            6,7
    0.4                            8,9
    0.5 Average                    10
    0.6                            11,12
    0.7                            13,14
    0.8                            15,16
    0.9                            17,18
    1   Unusually High Volume      19,20
```

Twitter Volume Discrepancies
-----------
```
    0   Unusually Low Volume       0,1
    0.1                            2,3
    0.2                            4,5
    0.3                            6,7
    0.4                            8,9
    0.5 Average                    10
    0.6                            11,12
    0.7                            13,14
    0.8                            15,16
    0.9                            17,18
    1   Unusually High Volume      19,20
```

200 Day Moving Average
-----------
```
    Compare stock price data against this calculation
```


5 Day Moving Average
-----------
```
    Compare stock price data against this calculation
```

Additional Data Used In Neural Network
-----------
```
    Trading Season
    Trading Day
    News Headlines
    Price Date               [Open, Low, High, Close]
    Tweet Likes
    User Sentiment
    Average Tweet Volume     [30 Days]
    Average Tweet Volume     [60 Days]
    Average Tweet Volume     [90 Days]
    Average News Headlines   [30 Days]
    Average Market Sentiment [30 Days]
    Average Trading Volume   [90 Days]
```

Initializing Neural Network
-----------
```
    network = Network()
    network.add_layer(8, 8, Network.ACTIVATION_SIGMOID) # Hidden Layer, 10 Neurons, 8 inputs
    network.add_layer(2, 8, Network.ACTIVATION_SIGMOID) # Output Layer,  2 Neurons, 8 inputs  
```

Configurations
-----------
```
  ITERATIONS = 500  
  LEARN_RATE = 0.03 
  THRESHOLD  = 0.001

```

Data Training
-----------
```
   for set in NeuralTraining:  
        print("Finding hidden Robots...")
        train = [
            set["TradingDay"],        set["TradingSeason"], 
            set["VolumeNormalized"],  set["AboveBigMoving"],
            set["BelowLittleMoving"], set["TweetsVolumeNormalized"], 
            set["Sentiment"],         set["Sentiment30"]
        ]
        Output1 = set["Output1"]
        Output2 = set["Output2"]
        error += network.train(train, [Output1, Output2], LEARN_RATE)
```

<img src="http://pablofernandez.com/stockmarket/imgs/A.png" alt="Sentiment Analysis" height="110px"/>
```
Positive:        64.08
Negative:        35.91
Neutral:         61.45

No Bullish / Bearish Indicator Detected
1x Likes                         x0.15 Score Boost / Ea

Final Analysis:  +31.0     [-100,100]
```

<img src="http://pablofernandez.com/stockmarket/imgs/B.png" alt="Sentiment Analysis" height="118px"/>

```
Positive:        29.58
Negative:        70.41
Neutral:         56.21

No Bullish / Bearish Indicator Detected

Final Analysis:  -41.0     [-100,100]  
```
<img src="http://pablofernandez.com/stockmarket/imgs/C.png" alt="Sentiment Analysis" height="130px"/>
```
Positive:        30.45
Negative:        69.54
Neutral:         74.91

Bearish Indicator Detected

Final Analysis:  -70.0     [-100,100]  
```

<img src="http://pablofernandez.com/stockmarket/imgs/D.png" alt="Sentiment Analysis" height="127px"/>
```

Positive:        36.84
Negative:        63.15
Neutral:         83.33

Bullish Indicator Detected
2x Likes                         x0.15 Score Boost / Ea

Final Analysis:  +48     [-100,100] 
```

Future Improvements
-----------
During extremelly big stock movements, either due to product releases or major announcements, the algorithm cannot
handle the massive amounts of Tweets (100s/second). Since the program runs every 15 mins, and is limited by StockTwits
API, some of the posts may not be saved in time. 

Additionally, implementation of more calculations using Headlines and other news in relation to a particular trading
day could be used in the future. 
