import json
import boto3
import os
from boto3.dynamodb.conditions import Key

def handler(event, context):
    if event.get('httpMethod') and event['httpMethod'] != 'GET':
        return {
        'statusCode': 405,
        'body': json.dumps({'message': 'Method Not Allowed, only GET is accepted'})
        }

    params = event.get('queryStringParameters') or {}
    user_id = params.get('id')
    email = params.get('email')

    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table_name = os.environ['STORAGE_USERS_NAME']
    table = dynamodb.Table(table_name)

    if user_id:
        response = table.get_item(Key={'id': user_id})
        user = response.get('Item')
    elif email:
        response = table.query(
            IndexName='emails',
            KeyConditionExpression=Key('email').eq(email)
        )
        user = response['Items'][0] if response['Items'] else None
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Paramètre id ou email requis'})
        }

    if not user:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Utilisateur non trouvé'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps(user)
    }
