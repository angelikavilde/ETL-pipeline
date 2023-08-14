"""File with connections to the database redshift and AWS bucket"""

from os import environ

from redshift_connector import connect, Connection
from dotenv import load_dotenv
from boto3 import client
from botocore.client import BaseClient


def get_connection_container() -> Connection:
    """Returns container connection to the redshift database"""
    load_dotenv()
    connection = connect(database=environ["DB_NAME"], user=environ["DB_USER"],
    password=environ["DB_PASSWORD"],port=environ["DB_PORT"],host=environ["DB_HOST"])
    return connection


def get_bucket_connection() -> BaseClient:
    """Returns connection to the AWS buckets"""
    return client("s3", aws_access_key_id = environ.get("ACCESS_KEY"),
                aws_secret_access_key = environ.get("SECRET_KEY"))
