import boto3


def connect():
    return boto3.resource('dynamodb', region_name='us-west-2')