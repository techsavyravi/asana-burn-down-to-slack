import os
from pymongo import MongoClient
from datetime import datetime, date, timedelta
import pandas as pd

MONGO_URL = os.getenv('MONGO_URL')
# MONGO_DRS_URL = os.getenv('MONGO_DRS_URL')


clientRead = MongoClient(MONGO_URL)

db = clientRead.iDreamCareer

# mydata = db.users.find({"referred_by": {"$exists": "true"}, "is_existing": True})


start = datetime(2021, 1, 7, 0, 0, 0)
end = datetime(2021, 1, 8, 0, 0, 0)


# for data in mydata:
#     print(data)

for i in range(0, 20):
    s = date.today()-timedelta(days=i)
    e = date.today()-timedelta(days=i-1)
    start = datetime(s.year, s.month, s.day, 0, 0, 0)
    end = datetime(e.year, e.month, e.day, 0, 0, 0)
    print(start)
    print(end)
    mydata = list(db.users.find({"createdAt": {"$gte": start, "$lt": end}}))
    referralUsers = 0
    for data in mydata:
        if("referred_by" in data):
            referralUsers += 1

    totalSignups = len(mydata)

    print(totalSignups, referralUsers)

    print("*****")
