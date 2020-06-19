import requests
import json
import configparser
import os

def send2Slack(welcome, body):
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + '/settings.ini')
    url = config['SLACK']['url']

    jsonPayload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hi Team :wave:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": welcome
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": body
                }
            }
        ]
    }
    payload = json.dumps(jsonPayload)
    headers = {
        'Content-type': 'application/json',
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text.encode('utf8'))


def send2SlackWithImage(welcome, body, imageUrl):
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + '/settings.ini')
    url = config['SLACK']['url']

    jsonPayload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hi Team :wave:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": welcome
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": body
                }
            }
        ],
        "attachments": [
            {
                "text": "And here’s an attachment!",
                "image_url": imageUrl
            }
        ]
    }
    payload = json.dumps(jsonPayload)
    headers = {
        'Content-type': 'application/json',
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text.encode('utf8'))
