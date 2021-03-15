import base64
import json
import zlib
import datetime
import os
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    data = zlib.decompress(base64.b64decode(event['awslogs']['data']), 16+zlib.MAX_WBITS)
    data_json = json.loads(data)
    log_json = json.loads(json.dumps(data_json["logEvents"][0], ensure_ascii=False))
    
    print(data_json)
    log_group = data_json['logGroup']

    print(log_json)
    message = log_json['message']

    try:
        publish_to_sns(log_group, message)

    except Exception as e:
        print(e)
        
def publish_to_sns(subject, message):
    sns = boto3.client('sns')

    #SNS Publish
    publishResponse = sns.publish(
        TopicArn = os.environ['SNS_TOPIC_ARN'],
        Message = message,
        Subject = subject
    )