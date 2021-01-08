import os
from pymongo import MongoClient

MONGO_URL = os.getenv('MONGO_URL')

client = MongoClient(MONGO_URL)

db = client.iDreamCareer

mydata = db.events.aggregate([{'$match': {"event_type": "login"}}, {'$group': {"_id": '$user_id', "count": {'$sum': 1}}}, {'$project': {
                             "name": '$_id', "count": '$count', "_id": 1}}, {'$group': {"_id": '$count', "count": {'$sum': 1}}}, {'$sort': {"_id": 1}}])

data1to10 = []
sumPost10 = {
    "logincount": 10,
    "count": 0
}
for data in mydata:
    if(data['_id'] >= 10):
        sumPost10['count'] = sumPost10['count'] + data['count']
    else:
        data1to10.append({
            "logincount": data["_id"],
            "count": data["count"]
        })

data1to10.append(sumPost10)

for item in data1to10:
    db.data1to10.update_one({
        "logincount": item['logincount']
    }, {
        "$set": item
    },
        upsert=True
    )

# total_inserted = db.data1to10.insert_many(data1to10)
# print(total_inserted)

print(data1to10)

myEngagementData = db.events.aggregate(
    [{
        '$match': {"event_type": "login"}
    }, {
        "$project": {
            "yearMonthDay": {"$dateToString": {"format": '%Y-%m-%d', "date": "$createdAt"}},
            "time": {"$dateToString": {"format": '%H:%M:%S:%L', "date": '$createdAt'}}
        }
    }, {
        '$group': {"_id": '$yearMonthDay', "count": {'$sum': 1}}
    },
        {
            '$sort': {"_id": 1}
    }
    ]
)

for data in myEngagementData:
    print(data)
