import os
import json
import urllib.request
import urllib.parse


def handler(event, context):
    sns = event['Records'][0]['Sns']
    subject = sns['Subject']
    message = sns['Message']
    send_to_slack(f'recieve message from {subject}: {message}')


def send_to_slack(message):
    print(message)
    url = os.environ['SLACK_WEBHOOK_URL']
    data = json.dumps({'text': message})
    data = data.encode('utf-8')
    request = urllib.request.Request(url, data)
    response = urllib.request.urlopen(request)
    html = response.read()
    print(f'send complete: response code={response.getcode()}, response={html.decode("utf-8")}')
