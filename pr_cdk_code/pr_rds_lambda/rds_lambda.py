import boto3
import base64
from botocore.exceptions import ClientError
import json
import pymysql as db
import logging
import csv
from io import StringIO


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

# logger.debug(f"Event: {event}")

def insert_into(insert_stmt, db_user, db_password, db_name, db_host, params=None):
    """
    Insert records into the database as a result of the insert statement
    :param insert_stmt: insert statement, typically with prepared statement parameters
    :param params: List of parameters
    :return: True - success, no execptions.  False - an error occurred
    """
    conn = None
    pk = None
    try:
        conn = db.connect(host=db_host,
                          port=3306,
                          user=db_user,
                          password=db_password,
                          database=db_name,
                          connect_timeout=5,
                          read_timeout=5)
        cursor = conn.cursor()
        cursor.execute(insert_stmt, params)
        if 'returning' in insert_stmt:
            pk = cursor.fetchone()[0]

        conn.commit()
    except Exception as exc:
        print(f"Could not insert/update record: Statement: {insert_stmt} with parameters: {params}.  Exc: {exc}")
    finally:
        if conn:
            conn.close()

    return pk

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

"""
S3 Event Example
{
   "Records":[
      {
         "eventVersion":"2.1",
         "eventSource":"aws:s3",
         "awsRegion":"us-east-1",
         "eventTime":"2020-08-30T20:46:52.185Z",
         "eventName":"ObjectCreated:Put",
         "userIdentity":{
            "principalId":"AWS:AIDAIPR4RVWVANBX5X2R4"
         },
         "requestParameters":{
            "sourceIPAddress":"73.45.246.157"
         },
         "responseElements":{
            "x-amz-request-id":"9188395DAA69AA87",
            "x-amz-id-2":"DxRHTwtPhItZohLhM+kCCVvSKn+4/GcS/z/4PAIlqOYkRHgUTGI17zNNR/sLZGR/897dZVJ9yX5G7W4SeZIAHBp6zO+v7CN7"
         },
         "s3":{
            "s3SchemaVersion":"1.0",
            "configurationId":"MzM0OGIxMzItMjk4OC00MmM1LWFkZDgtNGFiYmVkNzBlOWZj",
            "bucket":{
               "name":"pryan-cdk-rds-event-bucket",
               "ownerIdentity":{
                  "principalId":"A3CKUBHQ1QBY9A"
               },
               "arn":"arn:aws:s3:::pryan-cdk-rds-event-bucket"
            },
            "object":{
               "key":"test_rds_data.csv",
               "size":29,
               "eTag":"105dba8131f1f4175ab20956b4477902",
               "sequencer":"005F4C103D7D47D8B2"
            }
         }
      }
   ]
}
"""

def is_s3_event(event_record):
    if event_record:
        return event_record['eventSource'] == "aws:s3"
    else:
        return False

def get_bucket_filename(event_record):
    if event_record:
        return event_record['s3']['bucket']['name'], event_record['s3']['object']['key']
    else:
        return None, None

def get_s3_file_contents(bucket, path):
    session = boto3.session.Session()
    client = session.client(
        service_name='s3',
        region_name='us-east-1'
    )

    json_return = client.get_object(Bucket=bucket, Key=path)
    # read the contents which will be a byte array that has to be converted to a string
    file_contents = json_return['Body'].read()

    return file_contents.decode('utf-8')

def handler(event, context):
    print(f"**** {event}")

    resp = get_secret(secret_name='pryandev-rds-secret')

    print(resp)
    rds_password = json.loads(resp['SecretString'])['rds-password']
    rds_username = json.loads(resp['SecretString'])['username']

    param_value = get_param_value('/pryandev/db-host')
    db_host = param_value['Parameter']['Value']

    # for now hard code some stuff
    param_value = get_param_value('/pryandev/db-name')
    db_name = param_value['Parameter']['Value']

    results = run_query("SELECT * FROM pr_test_tbl", db_user=rds_username, db_password=rds_password, db_host=db_host, db_name=db_name)

    print(f"BEFORE INSERT: {len(results)}, {results}")

    if 'Records' in event:
        for record in event['Records']:
            if is_s3_event(record):
                bucket, file = get_bucket_filename(record)
                print(f"Bucket: {bucket}, File: {file}")
                file_contents = get_s3_file_contents(bucket, file)
                print(f"**** Contents: {file_contents}")
                file_buf = StringIO(file_contents)
                reader = csv.reader(file_buf)
                for row in reader:
                    print(row)
                    pk = insert_into("insert into pr_test_tbl (name) values (%s)", db_user=rds_username, db_password=rds_password, db_host=db_host, db_name=db_name, params=[row[0]])
                    print(f'Inserted row id: {pk}')


    results = run_query("SELECT * FROM pr_test_tbl", db_user=rds_username, db_password=rds_password, db_host=db_host, db_name=db_name)

    print(f"AFTER INSERT: {len(results)}, {results}")

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f'RDS Database has {len(results)} records\n'
    }

