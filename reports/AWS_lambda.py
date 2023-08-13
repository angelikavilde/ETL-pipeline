"""AWS Lambda function file"""

from previous_day_report import retrieve_yesterdays_transactions, make_html_report
from previous_day_report import make_json_report, make_report
from connections import get_connection_container


def lambda_handler(event = None, context = None) -> str:
    """Returns html table formatted findings"""
    connection = get_connection_container()

    yesterday_transactions = retrieve_yesterdays_transactions(connection)
    findings_report = make_report(yesterday_transactions)
    json_data = make_json_report(findings_report, False)
    return {"html" : make_html_report(json_data, False)}


if __name__ == "__main__":
    print(lambda_handler())
