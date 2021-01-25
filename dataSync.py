from getCCES import getCCES
from ScrollDepth import getScrollDepth
import os
from pymongo import MongoClient
from datetime import datetime, date, timedelta
import pandas as pd
from drawChart import plot_stacked_bar
import matplotlib.pyplot as plt
from get_engagement import getEngagement
from getCCES import getCCES
from slack import send2SlackCustomURL
MONGO_URL = os.getenv('MONGO_URL')
MONGO_DRS_URL = os.getenv('MONGO_DRS_URL')

def DAU(startitfrom = 0, till = 1):
    clientRead = MongoClient(MONGO_URL)
    clientDRS = MongoClient(MONGO_DRS_URL)

    db = clientRead.iDreamCareer
    dbDRS = clientDRS.reports

    BulkMongoDocs = []

    startfrom = startitfrom
    noofdaystodothisfor = startfrom + till

    for i in range(startfrom, noofdaystodothisfor):
        s = date.today()-timedelta(days=i)
        e = date.today()-timedelta(days=i-1)
        start = datetime(s.year, s.month, s.day, 0, 0, 0)
        end = datetime(e.year, e.month, e.day, 0, 0, 0)
        # print(start)
        # print(end)
        mydata = list(db.users.find({"createdAt": {"$gte": start, "$lt": end}}))
        myEngData = getEngagement(start, end, db, mydata)
        scollDepth = getScrollDepth(start, end, db)
        dailyCCES = getCCES(start, end, db)
        referralUsers = 0
        phoneNumbers=[]
        for data in mydata:
            # print(str(data['_id']))
            if("referred_by" in data):
                referralUsers += 1

        totalSignups = len(mydata)
        print(phoneNumbers)
        mongoDoc = {
            "day": start.day,
            "month": start.month,
            "year": start.year,
            "referral_count": referralUsers,
            "new_user_count": totalSignups-referralUsers,
            "engagement_count": myEngData,
            "clicks": dailyCCES,
            "timestamp": start
        }
        mongoDoc.update(scollDepth)
        print(mongoDoc)

        BulkMongoDocs.append(mongoDoc)
        collection=dbDRS.dau
        collection.replace_one({
            "day": start.day,
            "month": start.month,
            "year": start.year,
        }, mongoDoc, upsert= True)
        print(i)