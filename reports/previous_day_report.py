"""Creating a report of yesterday's data"""

from datetime import datetime, timedelta
from json import dumps

from json2html import *
from redshift_connector import Connection

from connections import get_connection_container


YESTERDAY_DATE = datetime.now() - timedelta(days=1)


def retrieve_yesterdays_transactions(conn: Connection):
    """Returns a dataframe of yesterdays truck transactions"""
    with conn.cursor() as cur:
        cur.execute("""SELECT truck_information.truck_name, SUM(total) sum_total,
                COUNT(total) AS number_of_transactions, AVG(total) AS mean,
            PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY total) AS median
            FROM sigma_angela_schema.transactions
            LEFT JOIN sigma_angela_schema.truck_information ON
            (transactions.truck_id=truck_information.truck_id)
            WHERE EXTRACT(DAY FROM timestamp) = %s
            GROUP BY truck_information.truck_name""", [YESTERDAY_DATE.day])
        data = cur.fetch_dataframe().round(2)
        data[['sum_total',"number_of_transactions","mean","median"]] = \
        data[['sum_total',"number_of_transactions","mean","median"]].astype(float)
        data.set_index(["truck_name"])
    return data


def make_report(data) -> dict:
    """Returns dict report of findings"""
    full_sum = data["sum_total"].sum()
    data = data.to_dict(orient="records")
    report = dict()
    report["Date"] = YESTERDAY_DATE.strftime("%Y-%m-%d")
    report["Trucks"] = dict()
    for truck in data:
        truck_copy = truck.copy()
        truck_copy.pop("truck_name", None)
        report["Trucks"][truck["truck_name"]] = truck_copy
    report["Full Total"] = full_sum
    return report


def make_json_report(data: dict, save: bool = True) -> str:
    """Creates JSON from dict with findings and returns it"""
    data = dumps(data, indent = 3)
    if save:
        save_file("json", data)
    return data


def save_file(filetype: str, data: dict | str) -> None:
    """Saves a file into reports dir"""
    date = YESTERDAY_DATE.strftime("%Y_%m_%d")
    with open(f"data/report_data_{date}.{filetype}", "w", encoding="UTF-8") as file:
        file.write(data)


def make_html_report(data: str, save: bool = True) -> str:
    """Creates HTML with findings from JSON type data"""
    html_data = json2html.convert(json = data)
    html_data = html_data.replace("_", " ")
    if save:
        save_file("html", html_data)
    return str(html_data)


if __name__ == "__main__":
    connection = get_connection_container()

    yesterday_transactions = retrieve_yesterdays_transactions(connection)
    findings_report = make_report(yesterday_transactions)
    json_data = make_json_report(findings_report)
    html = make_html_report(json_data)
