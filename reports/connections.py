"""File with connections to the database redshift"""

from os import environ

from redshift_connector import connect, Connection
from dotenv import load_dotenv


def get_connection_container() -> Connection:
    """Returns container connection to the redshift database"""
    load_dotenv()
    connection = connect(database=environ["DB_NAME"], user=environ["DB_USER"],
    password=environ["DB_PASSWORD"],port=environ["DB_PORT"],host=environ["DB_HOST"])
    return connection
