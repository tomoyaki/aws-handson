import json
import urllib.parse
import boto3

s3 = boto3.client('s3')
comprehend = boto3.client('comprehend')


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        
        #output_jsonからtranscriptを抽出
        body = json.load(response['Body'])
        transcript = body['results']['transcripts'][0]['transcript']
        
        #Comprehendを呼び出す
        sentiment_response = comprehend.detect_sentiment(
        Text=transcript,
        LanguageCode='ja'
        )
        
        #Comprehendの戻り値からスコアを抽出して出力する        
        sentiment_score = sentiment_response.get('SentimentScore')
        print(sentiment_score)
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
