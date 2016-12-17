Neural Markets
========

I have created an AI software program that is capable of tracking thousands of Tweets per minute to create actionable predictions in the stock market. The algorithm runs a sentiment analysis on all stocks being tracked, and combines this data with proven technical indicators to train the neural network. 


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
            set["DayOfWeek"],         set["TradingMonth"], 
            set["VolumeNormalized"],  set["AboveBigMoving"],
            set["BelowLittleMoving"], set["TweetsVolumeNormalized"], 
            set["Sentiment"],         set["Sentiment30"]
        ]
        Output1 = set["Output1"]
        Output2 = set["Output2"]
        error += network.train(train, [Output1, Output2], LEARN_RATE)
```

<img src="http://pablofernandez.com/stockmarket/imgs/A.png" alt="Sentiment Analysis" style="width: 50px;"/>
<img src="http://pablofernandez.com/stockmarket/imgs/B.png" alt="Sentiment Analysis" style="width: 50px;"/>
<img src="http://pablofernandez.com/stockmarket/imgs/C.png" alt="Sentiment Analysis" style="width: 50px;"/>
<img src="http://pablofernandez.com/stockmarket/imgs/D.png" alt="Sentiment Analysis" style="width: 50px;"/>

