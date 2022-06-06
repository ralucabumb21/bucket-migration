import os
from contextlib import contextmanager
from moto import mock_s3
import pytest
import boto3


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def s3_client(aws_credentials):
    with mock_s3():
        conn = boto3.client("s3", region_name="us-east-1")
        yield conn


@contextmanager
def s3_bucket(s3, bucket_name):
    s3.create_bucket(Bucket=bucket_name)
    yield


def test_list_buckets(s3_client, bucket_name='old-test-bucket'):
    with s3_bucket(s3_client, bucket_name):
        buckets = s3_client.list_buckets()
        print(buckets)
        assert buckets['Buckets'][0]['Name'] == 'old-test-bucket'


def test_put_and_copy_object(s3_client, bucket_name='old-test-bucket', bucket_name2='new-test-bucket', key='testing',
                             body='body'):
    with s3_bucket(s3_client, bucket_name):
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=body)
        object_response = s3_client.get_object(Bucket=bucket_name, Key=key)
        assert object_response['Body'].read().decode() == body
        with s3_bucket(s3_client, bucket_name2):
            source_bucket = {"Bucket": bucket_name, "Key": key, "Body": body}
            production_key = "testing2"
            s3_client.put_object(Bucket=bucket_name2, Key="testing2")
            copy_objects = s3_client.copy_object(CopySource=source_bucket, Bucket=bucket_name2,
                                                 Key=production_key,
                                                 TaggingDirective='COPY')
            objects = s3_client.get_object(Bucket=bucket_name2, Key='testing2')
            assert objects['Body'].read().decode() == body
            assert copy_objects['CopyObjectResult'] is not None
