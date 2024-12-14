import boto3
import os

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566"),
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )

def get_sqs_client():
    return boto3.client(
        'sqs',
        endpoint_url=os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566"),
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )