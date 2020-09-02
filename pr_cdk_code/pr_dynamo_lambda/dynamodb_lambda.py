import json
import requests
import os
import boto3

url = "https://randomuser.me/api/"

def get_random_user():
    response = requests.get(url, params={'dataType': 'json'})
    user = response.json()['results'][0]
    username = user['login']['username']

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

def handler(event, context):
    print('dynamodb_lambda: request: {}'.format(json.dumps(event)))

    ddb_table_name = os.getenv('DDB_TABLE_NAME')

    username, user = get_random_user()
    print(f"*** Add record for username: {username}")

    put_data(ddb_table_name, username, user)


    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f'Added Username: {username} to DynamoDB\n'
    }


if __name__ == '__main__':
    username, user = get_random_user()

    put_data('pryan-test-db', username, user, 'spr')

    print('done')
