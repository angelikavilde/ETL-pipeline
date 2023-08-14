"""Data gets uploaded to the psql"""

from os import remove

from redshift_connector import Connection
import pandas as pd

from connections import get_connection_container


def upload_transaction_data(conn: Connection, transactional_data: list[list[str]]) -> None:
    """Uploads transaction data to the database."""
    payment_types = {"card":1,"cash":2}
    transactional_data.set_index('truck_id', inplace=True)
    transactional_data["type"] = transactional_data["type"].replace(payment_types)
    records = transactional_data.to_records(column_dtypes=dict)
    add = []
    for item in records:
        add.append([int(val) if str(val).isdigit() else val for val in item])
    with conn.cursor() as cur:
        cur.executemany("""INSERT INTO sigma_angela_schema.transactions (truck_id,timestamp,
        payment_type_id,total) VALUES (%s,%s,%s,%s)""", add)
        conn.commit()


if __name__ == "__main__":
    connection = get_connection_container()

    filepath = "./data/data_combined.csv"
    data = pd.read_csv(filepath)
    upload_transaction_data(connection, data)
    remove(filepath)
