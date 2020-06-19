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
import os


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

totalStoryPointAtTheStartofTheSprint = 0
totalStoryPointTillNow = 0

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
            nextdaystart = day+datetime.timedelta(days=1)
            if taskcompletedate <= utc.localize(nextdaystart):
                for field in task['custom_fields']:
                    if field['name'] == 'Story Points':
                        completedStoryPoints += int(
                            field['enum_value']['name'])

    if(i == 1):
        totalStoryPointAtTheStartofTheSprint = totalStoryPoint
    totalStoryPointTillNow = totalStoryPoint
    print(completedStoryPoints)
    pendingStoryPoints = totalStoryPoint - completedStoryPoints
    i = i+1
    df.loc[i] = [day.strftime("%a, %d %b"),
                 pendingStoryPoints, completedStoryPoints]

    # print(day, totalStoryPoint, completedStoryPoints, pendingStoryPoints)
    totalStoryPoint = 0
    completedStoryPoints = 0

scopeCreepTillNow = ((totalStoryPointTillNow -
                      totalStoryPointAtTheStartofTheSprint)/totalStoryPointAtTheStartofTheSprint)*100

# df = df[:-1] # this deletes the last day from the pandas dataframe
print(df)

print(totalStoryPointAtTheStartofTheSprint,
      totalStoryPointTillNow, scopeCreepTillNow)

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

isUploaded = upload_to_aws(filename, "pre-somethings-" + filename)
os.remove(filename)

if(isUploaded != False):
    welcome = "*Here is todays's <https://en.wikipedia.org/wiki/Burn_down_chart|Burn Down Chart>.*"
    finalMessage = "This burn down chart shows *pending tasks in blue* and *completed task in orange*. The numbers written on *top* of each bar are total *<https://www.mountaingoatsoftware.com/blog/what-are-story-points|story points>* in the sprint on that particular day. The number written near the *blue bar's top edge* is the *pending story points*. The blue bar should continuously keep getting low and low (i.e. burning down) everyday and *eventually burn down to 0* towards the end of the sprint.\n\nTech team ensures that we keep our tasks moving on the kanban board in asana to ensure an accurate Burn Down Chart. It's a start, any shortcomings and enhancements to this will be overcome in future sprint's burn downs. "
    finalMessage += "\n\n*Scope Creep Till Today:* {0}%\n\n".format(
        str(round(scopeCreepTillNow)))
    addtofinal = ""
    if(scopeCreepTillNow > 20):
        addtofinal = "*[ALARMING] SCOPE CREEP IS ABOVE 20%. THIS MIGHT CAUSE SPILLOVERS*"
    if(scopeCreepTillNow > 30):
        addtofinal = "*[WARNING] SCOPE CREEP TOO HIGH. PLEASE DECIDE SPRINT JUDICIOUSLY*"
    if(scopeCreepTillNow > 50):
        addtofinal = "*[WARNING] SCOPE CREEP IS TOO HIGH.*"

    finalMessage += addtofinal

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
