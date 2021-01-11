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

BulkMongoDocs = []

startfrom = 1
noofdaystodothisfor = startfrom + 1

for i in range(startfrom, noofdaystodothisfor):
    s = date.today()-timedelta(days=i)
    e = date.today()-timedelta(days=i-1)
    start = datetime(s.year, s.month, s.day, 0, 0, 0)
    end = datetime(e.year, e.month, e.day, 0, 0, 0)
    # print(start)
    # print(end)
    mydata = list(db.users.find({"createdAt": {"$gte": start, "$lt": end}}))
    myEngData = getEngagement(start, end, db)
    referralUsers = 0
    for data in mydata:
        if("referred_by" in data):
            referralUsers += 1

    totalSignups = len(mydata)
   
    mongoDoc = {
        "day": start.day,
        "month": start.month,
        "year": start.year,
        "referral_count": referralUsers,
        "new_user_count": totalSignups-referralUsers,
        "engagement_count": myEngData,
    }
    BulkMongoDocs.append(mongoDoc)

sendString = "*Data for 10-01-2021*\n" + "*New Users (without ref):* " + str(BulkMongoDocs[0]['new_user_count']) + "\n*Referral Users:* " + str(BulkMongoDocs[0]['referral_count']) + "\n*Engagement Yesterday:* " + str(BulkMongoDocs[0]['engagement_count']) + "\n"
# print(sendString)
send2SlackCustomURL("Starting today, we'll have the last day's stats here on this channel everyday at 8:00am. Let's get crunching.", sendString, "https://hooks.sla ck.com/services/TPMAJ1G13/B01HYE4E3KR/DJauxGYrzH292mlgtpRiBkIA")