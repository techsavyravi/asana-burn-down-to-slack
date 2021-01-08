import os
from pymongo import MongoClient
from datetime import datetime, date, timedelta
import pandas as pd
from drawChart import plot_stacked_bar
import matplotlib.pyplot as plt

MONGO_URL = os.getenv('MONGO_URL')
MONGO_DRS_URL = os.getenv('MONGO_DRS_URL')


clientRead = MongoClient(MONGO_URL)

db = clientRead.iDreamCareer

# mydata = db.users.find({"referred_by": {"$exists": "true"}, "is_existing": True})


start = datetime(2021, 1, 7, 0, 0, 0)
end = datetime(2021, 1, 8, 0, 0, 0)


# for data in mydata:
#     print(data)

referralCounts = []
newUserCounts = []
category_labels = []

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
    date_time = start.strftime("%d-%m")

    referralCounts.append(referralUsers)
    newUserCounts.append(totalSignups-referralUsers)
    category_labels.append(date_time)
    print("*****")

# referralCounts.reverse()
# newUserCounts.reverse()
# category_labels.reverse()

# print(referralCounts, newUserCounts)

# plt.figure(figsize=(6, 20))

# series_labels = ['Series 1', 'Series 2']

# data = [
#     newUserCounts,
#     referralCounts
# ]

# # category_labels = ['Cat A', 'Cat B', 'Cat C', 'Cat D']

# plot_stacked_bar(
#     data, 
#     series_labels, 
#     category_labels=category_labels, 
#     show_values=True, 
#     value_format="{:.1f}",
#     colors=['tab:orange', 'tab:green'],
#     y_label="New Users"
# )

# plt.savefig('bar.png')
# plt.show()