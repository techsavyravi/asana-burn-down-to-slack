import os
from pymongo import MongoClient
from datetime import datetime, date, timedelta
import pandas as pd
from drawChart import plot_stacked_bar
import matplotlib.pyplot as plt
from get_engagement import getEngagement

MONGO_URL = os.getenv('MONGO_URL')
MONGO_DRS_URL = os.getenv('MONGO_DRS_URL')


clientRead = MongoClient(MONGO_URL)

db = clientRead.iDreamCareer

noofdaystodothisfor = 20
referralCounts = []
newUserCounts = []
category_labels = []
BulkMongoDocs = []

for i in range(0, noofdaystodothisfor):
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
    date_time = start.strftime("%d-%m")

    referralCounts.append(referralUsers)
    newUserCounts.append(totalSignups-referralUsers)
    category_labels.append(date_time)
    mongoDoc = {
        "day": start.day,
        "month": start.month,
        "year": start.year,
        "referral_count": referralUsers,
        "new_user_count": totalSignups-referralUsers,
        "engagement_count": myEngData,
    }
    print(mongoDoc)
    BulkMongoDocs.append(mongoDoc)
