import json
import boto3
import os
import uuid
import re
from boto3.dynamodb.conditions import Key

def handler(event, context):
    if event.get('httpMethod') and event['httpMethod'] != 'POST':
        return {
        'statusCode': 405,
        'body': json.dumps({'message': 'Method Not Allowed, only POST is accepted'})
        }

    body = json.loads(event['body'])
    name = body.get('name')
    email = body.get('email')

    if not name or not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Champs invalides'})
        }

    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table_name = os.environ['STORAGE_USERS_NAME']
    table = dynamodb.Table(table_name)

    existing = table.query(
        IndexName='emails',
        KeyConditionExpression=Key('email').eq(email)
    )

    if existing['Items']:
        return {
            'statusCode': 409,
            'body': json.dumps({'error': 'Email déjà utilisé'})
        }

    user_id = str(uuid.uuid4())

    table.put_item(
        Item={
            'id': user_id,
            'name': name,
            'email': email,
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Utilisateur ajouté', 'id': user_id})
    }
