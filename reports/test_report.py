"""File for testing functions in the report directory"""

from os import path, remove
import datetime
from unittest.mock import MagicMock

from previous_day_report import retrieve_yesterdays_transactions, make_html_report
from previous_day_report import make_json_report, make_report, save_file
from connections import get_connection_container


def test_get_connection_container(monkeypatch):
    """Verifies that fake connection was made"""
    monkeypatch.setattr("connections.connect", lambda database, user, password, port, host: None)
    assert get_connection_container() == None


def test_make_json_report():
    """Verifies that correctly formatted data is returned (json)"""
    assert make_json_report({"fake":"data"}, False) == '{\n   "fake": "data"\n}'


def test_make_html_report():
    """Verifies that correctly formatted data is returned (html)"""
    html_string = '<table border="1"><tr><th>fake</th><td>data</td></tr></table>'
    assert make_html_report('{\n   "fake": "data"\n}', False) == html_string


def test_make_report(data, monkeypatch):
    """Verifies that the report is made correctly from the data"""
    date = datetime.date(2023, 8, 12)
    monkeypatch.setattr("previous_day_report.YESTERDAY_DATE", date)

    assert make_report(data) == {'Date': date.strftime("%Y-%m-%d"), 'Full Total': 3,
    'Trucks': {'test': {'sum_total': 2}, 'test2': {'sum_total': 1}}}


def test_save_file(monkeypatch):
    """Verifies that the filepath is created and has correct input"""
    date = datetime.date(2023, 8, 12)
    monkeypatch.setattr("previous_day_report.YESTERDAY_DATE", date)
    date = date.strftime("%Y_%m_%d")
    filepath = f"data/report_data_{date}.csv"
    save_file("csv", "test")

    assert path.exists(filepath) is True

    with open(filepath, "r") as f:
        data = f.read()

    assert data == "test"
    remove(filepath)


def test_retrieve_yesterdays_transactions(transactions, returned_transactions):
    """Verifies that the function returns expected data"""
    fake_connection, fake_cursor = MagicMock(), MagicMock()
    fake_connection.cursor.return_value.__enter__.return_value = fake_cursor
    fake_cursor.fetch_dataframe.return_value = transactions

    assert retrieve_yesterdays_transactions(fake_connection).equals(returned_transactions)
