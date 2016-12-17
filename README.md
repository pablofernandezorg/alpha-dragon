Neural Markets
========

I have created an AI software program that is capable of tracking thousands of Tweets per minute to create actionable predictions in the stock market. The algorithm runs a sentiment analysis on all stocks being tracked, and combines this data with proven technical indicators to train the neural network. 








http://www.snowflakeco.com/live/software/recognition/api/CLOUD_ANALYZE.php?URL={ImageURL}


![Plate Image](ExampleResults.png "Input image")


User Guide
-----------

OpenALPR includes a command line utility.  Simply typing "alpr [image file path]" is enough to get started recognizing license plate images.

For example, the following output is created by analyzing this image:

![Plate Image](http://www.openalpr.com/images/demoscreenshots/plate3.png "Input image")



```
user@linux:~/openalpr$ alpr ./samplecar.png

plate0: top 10 results -- Processing Time = 58.1879ms.
    - PE3R2X     confidence: 88.9371
    - PE32X      confidence: 78.1385
    - PE3R2      confidence: 77.5444
    - PE3R2Y     confidence: 76.1448
    - P63R2X     confidence: 72.9016
    - FE3R2X     confidence: 72.1147
    - PE32       confidence: 66.7458
    - PE32Y      confidence: 65.3462
    - P632X      confidence: 62.1031
    - P63R2      confidence: 61.5089

```

Detailed command line usage:

```
user@linux:~/openalpr$ alpr --help

USAGE: 

   alpr  [-c <country_code>] [--config <config_file>] [-n <topN>] [--seek
         <integer_ms>] [-p <pattern code>] [--clock] [-d] [-j] [--]
         
         
         
         
         
         
        

Modules
-----------------------------------------------------
modify        #    Parsing Twitter Input Values
analysis      #    **CONFIDENTIAL Scoring Algorithm For Language & Trends
connection    #    **CONFIDENTIAL Server Database Authentication & Connection
fetchdata     #    Fetch Data From Twitter & Yahoo Finance 
pulldata      #    Pull Any Sort Of Information From The Database
insertdata    #    Insert Tweets & Stock Prices Into Database
update        #    Push Any Sort Of Update To The Database
