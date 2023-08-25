"""File with additions for testing"""

from datetime import datetime, timedelta, timezone
from os import environ

from pandas import DataFrame
import pandas as pd
from pytest import fixture
from boto3 import client
from botocore.client import BaseClient
from moto import mock_s3


class FakeConn:
    """Class for creating mock connections"""

    def cursor(self) -> 'FakeCursor':
        """Fakes a cursor object"""
        return FakeCursor()

    def commit(self) -> None:
        """Fakes connection commit"""
        pass


class FakeCursor:
    """Class for mocking a cursor"""

    def __enter__(self) -> 'FakeCursor':
        """Mocking opening with cursor"""
        return self

    def __exit__(self, *args) -> None:
        """Mocking closing with cursor"""
        pass

    def fetchall(self) -> list[list[int]]:
        """Mocking items received from cursor execute"""
        return [[1,8],[8,1]]

    def execute(self, query) -> None:
        """Mocking cursor.execute"""
        pass

    def executemany(self, *args) -> None:
        """Mocking cursor.executemany"""
        print("Executed!")


class FakeS3:
    """Class for testing fake methods of the s3"""

    def list_objects(self, Bucket) -> dict:
        """Function mocks list of objects in a bucket"""
        return {"Contents":[{"Key":"test/test3.csv", "LastModified": "01/01/22"},
                {"Key":"test/test4.csv", "LastModified": "11/21/22"}]}

    def download_file(self, *args) -> None:
        """Function that creates fake csv file and writes in it
        to then merge in other tests"""
        print("Magic happened!")


@fixture
def fake_files() -> list[tuple[str, datetime]]:
    """Returns list of items with name and time created"""
    date = datetime(2023, 8, 12, 6, 9, 2)
    two_hours_before = date - timedelta(hours=2)
    return [('trucks/2023-8/test3.csv', two_hours_before),
            ('trucks/2023-8/test4.csv', two_hours_before)]


@fixture
def transactions() -> DataFrame:
    """Returns a dataframe for tests"""
    cols = ["timestamp", "total", "type", "truck_id"]
    time1 = datetime(2023, 8, 12, 6, 9, 2, tzinfo=timezone.utc)
    time2 = datetime(2023, 8, 12, 6, 9, 12, tzinfo=timezone.utc)
    test_data = [[time1,5,"card",4],[time2,5.1,"cash",2]]
    return pd.DataFrame(data=test_data,columns=cols, index=["1","2"])


@fixture
def aws_credentials() -> None:
    """Mocked AWS Credentials for moto"""
    environ["SECRET_KEY"] = "testing"
    environ["ACCESS_KEY"] = "testing"


@fixture
def s3(aws_credentials) -> BaseClient:
    """Mocks the client"""
    with mock_s3():
        yield client("s3", region_name="us-east-1")
