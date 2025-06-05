import json
import boto3
from datetime import datetime
from decimal import Decimal
import os

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(i) for i in obj]
    return obj

def handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
        s3 = boto3.client('s3', region_name='eu-west-1')
        
        crypto_table_name = os.environ['STORAGE_CRYPTOPRICES_NAME']
        bucket_name = os.environ['STORAGE_CRYPTOSTORAGE_BUCKETNAME']
        
        table = dynamodb.Table(crypto_table_name)
        response = table.scan()
        items = response['Items']
        
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        
        cleaned_items = decimal_to_float(items)
        
        sorted_items = sorted(cleaned_items, key=lambda x: x['timestamp'])
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')
        file_key = f'exports/crypto_{timestamp}.json'
        
        json_data = json.dumps(sorted_items, indent=2)
        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json_data,
            ContentType='application/json'
        )
        
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': file_key
            },
            ExpiresIn=3600  # 1 heure en secondes
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({
                'message': 'Export successful',
                'url': url,
                'file_key': file_key
            })
        }
        
    except Exception as e:
        print('Error:', str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }