from datetime import datetime, date, timedelta


def getCCES(start, end, db):
    query = {
        "event_type": 'click',
        "createdAt": {"$gte": start, "$lt": end}
    }
    pipeline = [
        {"$match": query},
        {
            "$group": {
                "_id": "$content_type",
                "count": {"$sum": 1},
            },
        }
    ]

    # print(query)
    mydata = list(db.events.aggregate(pipeline))
    print(mydata)
    return mydata
