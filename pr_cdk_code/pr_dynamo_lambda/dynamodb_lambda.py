import json
import requests
import os
import boto3
from decimal import Decimal
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


url = "https://randomuser.me/api/"

def get_random_user():
    username = None
    user = None

    try:
        response = requests.get(url, params={'dataType': 'json'})
        user = response.json()['results'][0]
        username = user['login']['username']
    except:
        print("Error getting fake user")

    return username, user

def put_data(table_name,  pk, data, profile_name=None):
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.resource('dynamodb')

    table = dynamodb.Table(table_name)
    response = table.put_item(
       Item={
            'pk': pk,
            'user': data
        }
    )
    return response

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


def read_random_user(table_name, username, profile_name=None):
    session = boto3.Session(profile_name=profile_name)
    dynamodb = session.resource('dynamodb')

    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'pk': username})
    logger.debug(f"Username: {username}, Response: {json.dumps(response, default=default)}")

    item = response.get('Item', None)

    return item



def handler(event, context):
    logger.debug('dynamodb_lambda: request: {}'.format(json.dumps(event)))

    ddb_table_name = os.getenv('DDB_TABLE_NAME')

    body = 'Malformed request'

    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        if 'username' in event['queryStringParameters']:
            username = event['queryStringParameters']['username']
            user_item = read_random_user(ddb_table_name, username)
            if user_item:
                body = f'Username: {username} \nData: {json.dumps(user_item, default=default, indent=2)}\n'
            else:
                body = f'Could not find user for username: {username}\n'
    else:
        username, user = get_random_user()
        logger.debug(f"*** Add record for username: {username}")

        if username:
            put_data(ddb_table_name, username, user)
            get_user_url = f"https://{event['requestContext']['domainName']}{event['requestContext']['path']}?username={username}\n"
            body = f'Added Username: {username} to DynamoDB\nGet Details:\n{get_user_url}'
        else:
            body = f'Hmm... could not get a new person.  Try again in a minute\n'


    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': body
    }


if __name__ == '__main__':
    username, user = get_random_user()
    table_name = 'aws101a-stack-pryandevaws101ddb685940E7-9QQ496UEYS25'

    put_data(table_name, username, user, 'spr')
    item = read_random_user(table_name, username, 'spr')

    print(item)
