import json
import boto3 # boto3（AWSをpythonから操作するためのライブラリ）をインポート

translate = boto3.client('translate') # boto3を利用可能とする

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
		
	# json形式で出力する
    return {
        'statusCode': 200,
        'body': json.dumps({
          'output_text': output_text
        }),
        'isBase64Encoded':  False,
        'headers': {}
    }