import json
import requests


def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    ip_addr = requests.get('http://checkip.amazonaws.com').text.rstrip()
    print(f"*** IP Address: {ip_addr}")

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f'Hello, CDK! You have hit {event["path"]} at IP: {ip_addr}\n'
    }