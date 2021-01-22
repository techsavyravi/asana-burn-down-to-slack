from datetime import datetime, date, timedelta


def getEngagement(start, end, db, mydata):
    print(start)
    print(end)
    myIDs = []
    for data in mydata:
        myIDs.append(str(data['_id']))

    with open("z_newuser.txt", "w") as outfile:
        outfile.write("\n".join(myIDs))

    query = {
        "user_id": {
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
    pipeline1 = [
        {"$match": query},
        {
            "$group": {
                "_id": "$user_id",
                "logins": {"$sum": 1},
            },
        }
    ]

    # print(query)
    # mydata = list(db.events.aggregate(pipeline))
    myNumbers = list(db.events.aggregate(pipeline1))
    phoneNumbers=[]
    for data in myNumbers:
        phoneNumbers.append(data["_id"])
        # print(data['_id'])
    with open("z_returninguser.txt", "w") as outfile:
        outfile.write("\n".join(phoneNumbers))
    # print("******")
    # return mydata[0]['totalRepeatLogin'] if len(mydata) > 0 else 0
    return len(phoneNumbers)
