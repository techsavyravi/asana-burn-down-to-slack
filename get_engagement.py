from datetime import datetime, date, timedelta


def getEngagement(start, end, db, mydata):
    print(start)
    print(end)
    myIDs = []
    for data in mydata:
        myIDs.append(data['_id'])
    # print(myIDs)
    # pipeline = [
    #     {
    #         "$match": {
    #             "createdAt": {
    #                 "$lt": end,
    #                 "$gte": start
    #             },
    #         }
    #     },
    #     {
    #         "$group": {
    #             "_id": "$user_id",
    #             "logins": {"$sum": 1},
    #         },
    #     },
    #     {
    #         "$match": {
    #             "logins": {"$gt": 1},
    #             "users": {"$elemMatch": {"createdAt": {"$lt": end, "$gte": start}}}
    #         }
    #     },
    #     {
    #         "$project": {"users": 0}
    #     },
    #     {
    #         "$count": "totalRepeatLogin"
    #     }
    # ]
    query = {
        "_id": {
            "$nin": myIDs
        },
        "createdAt": {"$gte": start, "$lt": end}
    }
    pipeline = [
        {"$match": query},
        {
            "$group": {
                "_id": "$user_id",
                "logins": {"$sum": 1},
            },
        },
        {
            "$count": "totalRepeatLogin"
        }
    ]

    # print(query)
    mydata = list(db.events.aggregate(pipeline))
    return mydata[0]['totalRepeatLogin'] if len(mydata) > 0 else 0
