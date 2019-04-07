"""KickTranscribeWav2Txt"""
"""S3バケットにファイル生成されると起動する。起動条件はLambdaのS3トリガーにて指定"""

from boto3 import client
import urllib.parse
import datetime
import os

# 環境変数
URL_BASE = os.environ['URL_BASE']
REGION_NAME = os.environ['REGION_NAME']
ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']

def lambda_handler(event, context):

    input_key    = event['Records'][0]['s3']['object']['key']
#    input_key = urllib.parse.quote(input_key)

    source_file_uri = URL_BASE + input_key

    now = datetime.datetime.now()
    jobname = 'transcribejob_{0:%Y%m%d%H%M%S}'.format(now)

    transcribe_client = client("transcribe",
        region_name=REGION_NAME,
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY
        )

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=jobname,
        LanguageCode="en-US",
        MediaFormat="wav",
        Media={
            "MediaFileUri": source_file_uri
        }
    )
