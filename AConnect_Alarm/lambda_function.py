import boto3
import json
import os
import requests

# slackの設定
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
HOOK_URL      = os.environ['HOOK_URL']

def lambda_handler(event, context):

    # SNSイベントを取得
    message_unicode = event['Records'][0]['Sns']['Message']
    # 文字列から辞書型に変換
    message_dist = json.loads(message_unicode)
    # 各データを取得
    alarm_name  = message_dist['AlarmName']
#    description = message_dist['AlarmDescription']
    new_state   = message_dist['NewStateValue']
    reason      = message_dist['NewStateReason']

    if new_state == 'OK':
        emoji = ":+1:"
    elif new_state == 'ALARM':
        emoji = ":exclamation:"

    slack_message = {
        'channel': SLACK_CHANNEL,
        'text': "*%s %s: %s*\n Reason:%s" % (emoji, new_state, alarm_name, reason)
    }

    r = requests.post(HOOK_URL, data=json.dumps(slack_message))
