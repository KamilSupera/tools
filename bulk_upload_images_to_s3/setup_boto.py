from dotenv import load_dotenv

import os

import boto3
import logging

from botocore.exceptions import ClientError

load_dotenv()
logging.basicConfig(level=logging.INFO)

def setup_boto3_client(service: str = None):
    return boto3.client(
        service_name=service,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION_NAME")
    )


def upload_file_to_s3(client, file_name):
    path = os.getenv("FILE_PATH")
    bucket = os.getenv("AWS_S3_BUCKET_NAME")

    file_path = f"{path}{file_name}"

    try:
        client.upload_file(Filename=file_path, Bucket=bucket, Key=file_name)

        logging.info(f"File: {file_name} uploaded to S3")
    except ClientError as e:
        logging.error(f"File: {file_name} failed to upload to S3. Error: {e}")

        return False

    return True
