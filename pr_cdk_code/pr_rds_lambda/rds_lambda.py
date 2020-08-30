import boto3
import base64
from botocore.exceptions import ClientError
import json
import pymysql as db
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

# logger.debug(f"Event: {event}")

def run_query(query, db_user, db_password, db_name, db_host, params=None):
    conn = None
    results = None
    try:
        conn = db.connect(host=db_host,
                          port=3306,
                          user=db_user,
                          password=db_password,
                          database=db_name,
                          connect_timeout=10,
                          read_timeout=10)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()

    except Exception as exc:
        print(f"Could not execute query: Statement: {query} with parameters: {params}.  Exc: {exc}")
    finally:
        if conn:
            conn.close()
    return results

def get_param_value(parameter_name, decrypt=False, region_name='us-east-1', profile_name=None):
    session = boto3.session.Session(profile_name=profile_name)
    client = session.client(
        service_name='ssm',
        region_name=region_name
    )

    value = client.get_parameter(Name=parameter_name, WithDecryption=decrypt)

    return value

def get_secret(secret_name, region_name='us-east-1', profile_name=None):

    # Create a Secrets Manager client
    session = boto3.session.Session(profile_name=profile_name)
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        return get_secret_value_response
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])


def handler(event, context):
    resp = get_secret(secret_name='pryandev-rds-secret')

    print(resp)
    rds_password = json.loads(resp['SecretString'])['rds-password']
    rds_username = json.loads(resp['SecretString'])['username']

    param_value = get_param_value('/pryandev/db-host')
    db_host = param_value['Parameter']['Value']

    db_host = 'rpxg0ixv32oh13.ct3h2xhtmqys.us-east-1.rds.amazonaws.com'

    # for now hard code some stuff
    db_name = 'pryancdkdb'

    results = run_query("SELECT * FROM pr_test_tbl", db_user=rds_username, db_password=rds_password, db_host=db_host, db_name=db_name)

    print(results)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f'RDS Database has {len(results)} records\n'
    }

