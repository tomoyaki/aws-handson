const Aws = require('aws-sdk');
const Translate = new Aws.Translate({region: 'us-east-1'});
var docClient = new Aws.DynamoDB.DocumentClient({region: 'ap-northeast-1'});

    var date = new Date() ;
    var nowtime = date.getTime() ;


exports.handler = async (event) => {

    console.log('event ：' + JSON.stringify(event));
    let js = JSON.stringify(event);
    let body = JSON.parse(js);

    let js_body_text = event['queryStringParameters']['input_text'];
    //日本語から英語に翻訳
    let rs = await getAwsTranslate(js_body_text,'ja','en');
    global.rstext = rs.TranslatedText

    return {
        "statusCode": 200,
        "body": JSON.stringify({
            "output_text": rs.TranslatedText,
            "timestamp": nowtime,
            "input": js_body_text,
            "output": global.rstext
        }),
        "isBase64Encoded": false,
        "headers": {}
    }}

    var item = {
      timestamp: nowtime.toString(),
      input: "input",
      output: "output"
    };

    var params = {
      TableName: 'translate-history-2',
      Item: item
    };

    docClient.put(params, function (err, data) {
      if (err) {
          console.log(err);
      } else {
          console.log(data);
      }
    })
    
function getAwsTranslate(js_text,in_Language,out_Language) {
    return new Promise(((resolve, reject) => {
        let params = {
            Text: js_text,
            SourceLanguageCode: in_Language,
            TargetLanguageCode: out_Language
        }
        Translate.translateText(params, function(err,data){
            if (err) {
                console.log(err);
                reject();
            } else {
                console.log(JSON.stringify(data));
                resolve(data);
            }
        });
    }));
};