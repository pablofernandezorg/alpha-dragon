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

import re

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
 
def sanitize_data(data):
    if data is not None:
        # Remove Special Characters From String ************************    
        data = re.sub("[^a-zA-Z0-9-_*#%&?:;$()-<+>=!.]", " ", data)
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+", flags=re.UNICODE)
        data       = emoji_pattern.sub(r'', data)        
        emoji_pattern2 = re.compile(u'['
            u'\U0001F300-\U0001F64F'
            u'\U0001F680-\U0001F6FF'
            u'\u2600-\u26FF\u2700-\u27BF]+', 
            re.UNICODE)
        data = emoji_pattern2.sub(r'', data)
        emoji_pattern3 = re.compile(u'('
            u'\ud83c[\udf00-\udfff]|'
            u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
            u'[\u2600-\u26FF\u2700-\u27BF])+', 
            re.UNICODE)
        data = emoji_pattern3.sub(r'', data)
        data = data.replace("&#39;", "'")
        data = data.replace("&amp;", "&")
        data = " ".join(data.split())
        data = data.lstrip(' ')
        data.encode('utf-8')        
        return data
    else:
        data = "Empty"
        return data