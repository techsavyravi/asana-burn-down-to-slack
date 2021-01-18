import os
from pymongo import MongoClient
from datetime import datetime, date, timedelta
import pandas as pd
from drawChart import plot_stacked_bar
import matplotlib.pyplot as plt
from get_engagement import getEngagement
from slack import send2SlackCustomURL

MONGO_URL = os.getenv('MONGO_URL')
MONGO_DRS_URL = os.getenv('MONGO_DRS_URL')


clientRead = MongoClient(MONGO_URL)

db = clientRead.iDreamCareer

def getScrollDepth(start, end, db):
    matchQuery = {"$match": {"event_type": 'scroll-depth', "pageName": 'Dashboard', "createdAt": {"$gte": start, "$lt": end}}}
    mydata = list(db.events.aggregate([
        matchQuery,
        {"$group": {"_id": "$user_id", "maxValue": {"$max": "$scrollPercentage"}}},
        {"$match": {"maxValue": {"$gte": 0, "$lt": 25}}},
        {"$count": "mycount"}
    ]))

    ZeroToTwentyFive = mydata[0]['mycount'] if len(mydata) > 0 else 0 

    mydata = list(db.events.aggregate([
        matchQuery,
        {"$group": {"_id": "$user_id", "maxValue": {"$max": "$scrollPercentage"}}},
        {"$match": {"maxValue": {"$gte": 25, "$lt": 50}}},
        {"$count": "mycount"}
    ]))
    TwentyFiveToFifty = mydata[0]['mycount'] if len(mydata) > 0 else 0 

    mydata = list(db.events.aggregate([
        matchQuery,
        {"$group": {"_id": "$user_id", "maxValue": {"$max": "$scrollPercentage"}}},
        {"$match": {"maxValue": {"$gte": 50, "$lt": 75}}},
        {"$count": "mycount"}
    ]))
    FiftyToSeventyFive = mydata[0]['mycount'] if len(mydata) > 0 else 0 

    mydata = list(db.events.aggregate([
        matchQuery,
        {"$group": {"_id": "$user_id", "maxValue": {"$max": "$scrollPercentage"}}},
        {"$match": {"maxValue": {"$gte": 75, "$lt": 100}}},
        {"$count": "mycount"}
    ]))

    SeventyFiveToNintyNine = mydata[0]['mycount'] if len(mydata) > 0 else 0 


    mydata = list(db.events.aggregate([
        matchQuery,
        {"$group": {"_id": "$user_id", "maxValue": {"$max": "$scrollPercentage"}}},
        {"$match": {"maxValue": 100}},
        {"$count": "mycount"}
    ]))

    Hundred = mydata[0]['mycount'] if len(mydata) > 0 else 0 


    obj = {
        "ZeroToTwentyFive": ZeroToTwentyFive,
        "TwentyFiveToFifty": TwentyFiveToFifty,
        "FiftyToSeventyFive": FiftyToSeventyFive,
        "SeventyFiveToNintyNine": SeventyFiveToNintyNine,
        "Hundred": Hundred

    }
    return obj
    # print(obj)