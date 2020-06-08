import requests
import json
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymongo
import datetime
import configparser
import dateutil.parser
from validate_project import isProjectValid
import sys
import pytz
from utils import upload_to_aws
from slack import send2SlackWithImage


utc = pytz.UTC


config = configparser.ConfigParser()
config.read('settings.ini')

mongo_url = config['MONGO']['url']
url = "https://app.asana.com/api/1.0/projects/{0}".format(
    config['ASANA']['project_id'])

payload = {}
headers = {
    'Authorization': 'Bearer {0}'.format(config['ASANA']['bearer_token'])
}

response = requests.request("GET", url, headers=headers, data=payload)
y = json.loads(response.text.encode('utf8'))


startdate = datetime.datetime.strptime(y['data']['start_on'], "%Y-%m-%d")
enddate = datetime.datetime.strptime(y['data']['due_date'], "%Y-%m-%d")

print(startdate)
print(enddate)


sprint_days = pd.date_range(
    start=startdate, end=enddate).to_pydatetime().tolist()

y = isProjectValid(True)

if(y == False):
    sys.exit("Validation Failed. Team alerted on slack.")

# for day in sprint_days:
totalStoryPoint = 0
completedStoryPoints = 0
pendingStoryPoints = 0

df = pd.DataFrame(columns=['Day', 'Pending', 'Completed'])

i = 0
for day in sprint_days:
    if day > datetime.datetime.today():
        break
    for task in y['data']:
        taskcreatedate = dateutil.parser.parse(task['created_at'])
        if taskcreatedate <= utc.localize(day):
            for field in task['custom_fields']:
                if field['name'] == 'Story Points':
                    totalStoryPoint += int(field['enum_value']['name'])
        if task['completed']:
            taskcompletedate = dateutil.parser.parse(task['completed_at'])
            if taskcompletedate <= utc.localize(day):
                for field in task['custom_fields']:
                    if field['name'] == 'Story Points':
                        completedStoryPoints += int(
                            field['enum_value']['name'])

    pendingStoryPoints = totalStoryPoint - completedStoryPoints
    i = i+1
    df.loc[i] = [day.strftime("%a, %d %b"),
                 pendingStoryPoints, completedStoryPoints]

    # print(day, totalStoryPoint, completedStoryPoints, pendingStoryPoints)
    totalStoryPoint = 0
    completedStoryPoints = 0

print(df)

filename = datetime.datetime.today().strftime("%Y-%m-%d.png")
print(filename)

x = df[['Day', 'Pending', 'Completed']]
y = x.set_index('Day')

stackedPlot = y.plot.bar(stacked=True)


for i, label in enumerate(list(df.index)):
    total = df.values[i][1] + df.values[i][2]
    pending = df.values[i][1]
    stackedPlot.annotate(str(total), (i - 0.23, total + 0.4), color='blue')
    stackedPlot.annotate(
        str(pending), (i - 0.23, pending - 4.4), color='orange')

# plt.show()

fig = stackedPlot.get_figure()
fig.savefig(filename, bbox_inches="tight")

isUploaded = upload_to_aws(filename, filename)

if(isUploaded != False):
    welcome = "*Here is today's Burn Down Chart.*"
    finalMessage = "This burn down chart shows *pending tasks in blue* and *completed task in orange*. The numbers written on *top* of each bar are *total story points* for that particular day. The number written after near the *blue bar's top edge* is the *pending story points*. The blue bar should continuously keep getting low and low (i.e. burning down) everyday and *eventually burn down to 0* towards the end of the sprint.\n\nPlease ensure that you keep your tasks up to date in asana to ensure an accurate Burn Down Chart."
    send2SlackWithImage(welcome, finalMessage, isUploaded)

# plt.show(block=True)

# totalTasks = len(y['data'])
# print(totalTasks)
# totalStoryPoints = 0
# completedStoryPoints = 0
# scopeCreepStoryPoints = 0

# for task in y['data']:
#     for field in task['custom_fields']:
#         if field['name'] == 'Story Points':
#             if field['enum_value'] is not None:
#                 if task['completed']:
#                     completedStoryPoints += int(field['enum_value']['name'])
#                 for tag in task['tags']:
#                     if tag['name'] == 'SCOPE-CREEP':
#                         scopeCreepStoryPoints += int(
#                             field['enum_value']['name'])
#                 totalStoryPoints += int(field['enum_value']['name'])

# incompleteStoryPoints = totalStoryPoints - completedStoryPoints

# print(totalStoryPoints, incompleteStoryPoints,
#       completedStoryPoints, scopeCreepStoryPoints)

# arr = np.array([totalStoryPoints, incompleteStoryPoints,
#       completedStoryPoints, scopeCreepStoryPoints])

# plt.plot(arr)
# # plt.show()

# myclient = pymongo.MongoClient(mongo_url)

# mydb = myclient["stats"]
# mycol = mydb["asana"]

# mydict = { "timestamp": datetime.datetime.now(), "totalStoryPoints" : totalStoryPoints, "incompleteStoryPoints": incompleteStoryPoints, "completedStoryPoints": completedStoryPoints, "scopeCreepStoryPoints": scopeCreepStoryPoints }

# x = mycol.insert_one(mydict)

