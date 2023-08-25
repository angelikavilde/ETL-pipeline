"""File for testing functions in the pipeline directory"""

from datetime import datetime
from os import path, remove

import pandas as pd
from pytest import raises
from botocore.client import BaseClient

from conftest import FakeS3, FakeConn
from connections import get_connection_container
from extract import get_items_in_buckets, download_new_files
from transform import combine_transaction_data_files
from clean_data import get_trucks_no_card_reader, clean_the_dataset
from load import upload_transaction_data


def test_get_connection_container(monkeypatch):
    """Verifies that fake connection to the db was made"""
    monkeypatch.setattr("connections.connect", lambda **kwargs: None)
    assert get_connection_container() == None


def test_get_bucket_connection(s3):
    """Verifies that fake connection to the s3 bucket was made"""
    from connections import get_bucket_connection
    assert isinstance(get_bucket_connection(),BaseClient)


def test_get_items_in_buckets():
    """Tests that items in buckets were received in the correct form"""
    fake_conn = FakeS3()
    expected_result = [('test/test3.csv', '01/01/22'), ('test/test4.csv', '11/21/22')]
    assert get_items_in_buckets(fake_conn, "") == expected_result


def test_download_new_files(monkeypatch, capfd, fake_files):
    """Tests that a new file was downloaded whilst mocking
    the downloading aspect"""
    fake_conn = FakeS3()
    date = datetime(2023, 8, 12, 6, 9, 2)
    monkeypatch.setattr("extract.TIME_NOW", date)
    download_new_files(fake_conn, "", fake_files)
    captured = capfd.readouterr()

    assert "Magic" in captured.out.strip()


def test_combine_transaction_data_files():
    """Tests that the combined csv file was created"""
    file1 = "test/_T1_.csv"
    file2 = "test/_T2_.csv"

    with open(file1, "w") as f:
        f.write("1,2,3")
    with open(file2, "w") as f:
        f.write("1,2,3")

    combine_transaction_data_files([file1, file2])
    filepath = "data/data_combined.csv"

    assert path.exists(filepath)

    with open(filepath, "r") as f:
        data = f.read()

    assert "truck_id" in data
    remove(filepath)
    remove(file1)
    remove(file2)


def test_get_trucks_no_card_reader():
    """Tests that correct trucks were received"""
    assert (get_trucks_no_card_reader(FakeConn())) == {1,8}


def test_clean_the_dataset(transactions, monkeypatch):
    """Tests that only correct data was placed into the file"""
    monkeypatch.setattr("pandas.read_csv", lambda file: transactions)
    monkeypatch.setattr("os.remove", lambda file: print("File removed"))
    monkeypatch.setattr("clean_data.get_trucks_no_card_reader", lambda con: {1,8})
    filepath = "test/pd_test.csv"
    clean_the_dataset(FakeConn(),filepath)

    with open(filepath, "r") as f:
        cleaned_data = f.readlines()

    assert cleaned_data[1] == "2023-08-12 06:09:02+00:00,5.0,card,4\n"

    with raises(IndexError):
        cleaned_data[2]


def test_upload_transaction_data(capfd):
    """Tests that data was uploaded with connection and cursor objects"""
    filepath = "test/pd_test.csv"
    data = pd.read_csv(filepath)
    upload_transaction_data(FakeConn(),data)
    captured = capfd.readouterr()[0]

    assert "Executed!" in captured

    remove(filepath)
