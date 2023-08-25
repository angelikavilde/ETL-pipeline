"""File that cleans the data received"""

from datetime import datetime, timezone
import os

import pandas as pd
from redshift_connector import Connection

from connections import get_connection_container


def get_trucks_no_card_reader(conn: Connection) -> set[int]:
    """Returns distinct truck IDs without a card-reader"""
    with conn.cursor() as cur:
        cur.execute("""SELECT truck_id FROM sigma_angela_schema.truck_information
                     WHERE has_card_reader = 'NO'""")
        data = cur.fetchall()
    return set(j for i in data for j in i)


def clean_the_dataset(conn: Connection, filepath: str) -> None:
    """Function to clean the data"""
    truck_transactions = pd.read_csv(filepath)
    truck_transactions["total"] = pd.to_numeric(truck_transactions["total"], errors="coerce")
    truck_transactions = truck_transactions.dropna(subset=["total"])
    too_high_for_total = truck_transactions["total"].quantile(0.95)
    truck_transactions = truck_transactions[truck_transactions["total"] <= too_high_for_total]
    truck_transactions = truck_transactions[truck_transactions["total"] > 0]
    truck_transactions = truck_transactions[truck_transactions["type"].isin(["card","cash"])]
    no_card_reader = get_trucks_no_card_reader(conn)
    truck_transactions = truck_transactions[~((truck_transactions["truck_id"].isin(no_card_reader))
                             & (truck_transactions["type"] == "card"))]
    truck_transactions["timestamp"] = pd.to_datetime(truck_transactions["timestamp"], errors="coerce")
    truck_transactions = truck_transactions.dropna(subset=["timestamp"])
    truck_transactions = truck_transactions[truck_transactions["timestamp"] < datetime.now(timezone.utc)]
    os.remove(filepath)
    truck_transactions.to_csv(filepath, index=False)


if __name__=="__main__":
    connection = get_connection_container()

    clean_the_dataset(connection, "./data/data_combined.csv")
