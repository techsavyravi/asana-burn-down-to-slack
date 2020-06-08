import requests
import json
from slack import send2Slack
import configparser

def isProjectValid(informSlack=False):
    config = configparser.ConfigParser()
    config.read('settings.ini')

    url = "https://app.asana.com/api/1.0/projects/{0}/tasks?opt_pretty&opt_expand=(this%7Csubtasks%2B)".format(
        config['ASANA']['project_id'])

    payload = {}
    headers = {
        'Authorization': 'Bearer {0}'.format(config['ASANA']['bearer_token'])
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    y = json.loads(response.text.encode('utf8'))
    strypointmissing = ""
    assigneemissing = ""
    for task in y['data']:
        taskname = task['name']
        notes = task['notes']
        assigned_to = ""
        for field in task['custom_fields']:
            if field['name'] == 'Story Points':
                if field['enum_value'] is None:
                    strypointmissing += "<https://app.asana.com/0/{0}/".format(config['ASANA']['project_id']) + \
                        task['gid'] + "|" + task['name'] + ">\n"
        if task['assignee'] is None:
            assigneemissing += "<https://app.asana.com/0/{0}/".format(config['ASANA']['project_id']) + \
                task['gid'] + "|" + task['name'] + ">\n"

    welcome = "I was going through the <https://app.asana.com/0/{0}|current sprint> and found that we have a few missing elements which might block our progress and decrease our transprancy as a team. Why don't we fix it? Here are a few of them".format(
        config['ASANA']['project_id'])

    isValid = True
    if strypointmissing != "":
        strypointmissing = "*Story Points Missing*\n" + strypointmissing
        isValid = False
    if assigneemissing != "":
        assigneemissing = "*Assignee Missing*\n" + assigneemissing
        isValid = False

    if(not isValid and informSlack):
        finalMessage = strypointmissing + assigneemissing + \
            "\n *I'll check again in an hour. Let's fix it by then.*"
        send2Slack(welcome, finalMessage)
    
    if(isValid):
        return y
    else:
        return False