#!/usr/local/bin/python
# -*- coding: utf-8 -*-
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
 
import re

def remove_emoji(data):
    if data is not None:
        data = str(data)
        # Remove Special Characters From Tweet ************************
        # This line does not work on the server:
        #data       = data.translate ({ord(c): " " for c in "→!@#%^&*()[]{};:,./<>?\|`~-=_+"})
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
        data = re.sub(r'\W+', ' ', data)
        return data
    else:
        data = "Empty"
        return data
