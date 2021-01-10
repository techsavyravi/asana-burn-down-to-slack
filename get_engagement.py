from datetime import datetime, date, timedelta


def getEngagement(start, end, db):
    print(start)
    print(end)
    pipeline = [
        {
            "$match": {
                "createdAt": {
                    "$lt": end
                },
                "event_type": 'login'
            }
        },
        {
            "$sort": {"createdAt": - 1}
        },
        {
            "$group": {
                "_id": "$user_id",
                "logins": {"$sum": 1},
                "users": {"$push": "$$ROOT"},
            },
        },
        {
            "$match": {
                "logins": {"$gt": 1},
                "users": {"$elemMatch": {"createdAt": {"$lt": end, "$gte": start}}}
            }
        },
        {
            "$project": {"users": 0}
        },
        {
            "$count": "totalRepeatLogin"
        }
    ]

    mydata = list(db.events.aggregate(pipeline))
    return mydata[0]['totalRepeatLogin']
