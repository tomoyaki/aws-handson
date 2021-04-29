import json
import boto3 # boto3（AWSをpythonから操作するためのライブラリ）をインポート
import datetime

translate = boto3.client('translate') # boto3を利用可能とする

dynamodb_translate_history_tbl = boto3.resource('dynamodb').Table('translate-history') # DynamoDBのAPI

def lambda_handler(event, context):

    input_text = event['queryStringParameters']['input_text']
    
	# request syntaxを参考にinputとなるtext、source languageとtarget languageを設定
    response = translate.translate_text(
      Text=input_text,
      SourceLanguageCode='ja',
      TargetLanguageCode='en'
    )
		
	# response syntaxを参考にtranslatedtextを取得
    output_text = response.get('TranslatedText')
	
	# Dynamo DBにresponseを格納
    dynamodb_translate_history_tbl.put_item(
		  Item = {
		    'timestamp': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
		    'input_text': input_text,
		    'output_text': output_text
		  }
	  )
		
	# json形式で出力する
    return {
        'statusCode': 200,
        'body': json.dumps({
          'output_text': output_text
        }),
        'isBase64Encoded':  False,
        'headers': {}
    }