"""OutputTranscribedResult"""
"""Transcribeの結果ステータスをCloudWatchから受け取り動作する"""

import json
import logging
import urllib.request
import boto3
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
transcribe = boto3.client('transcribe')
sns = boto3.client('sns')

# 環境変数
SNS_ARN = os.environ['SNS_ARN']


def lambda_handler(event, context):
    logger.info(event)
    job_name = event['detail']['TranscriptionJobName']
    job_status = event['detail']['TranscriptionJobStatus']
 
    if job_status in ['COMPLETED']:
        # ジョブが成功した場合のみ呼び出す
        logger.info("COMPLETED")
        job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        logger.info(job)
        logger.info(job['TranscriptionJob']['Transcript'])

        url = job['TranscriptionJob']['Transcript']['TranscriptFileUri']

        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            body = json.load(res)
        message = body['results']['transcripts'][0]['transcript']

        # Mail送信
        response = sns.publish(
            TopicArn = SNS_ARN,
            Message = message,
            Subject = u'Transcribe jobname ' + job_name
        )
        logger.info("MAIL SEND")
        return job['TranscriptionJob']['Transcript']

    elif job_status in ['FAILED']:
        # ジョブが失敗した場合の処理は今回は未実装
        logger.info("FAILED")
        pass

    else:
        logger.error("Unknown Status Found : {}".format(job_status))
#        raise Exception

