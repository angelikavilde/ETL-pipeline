"""Extracting data from buckets every 3hrs when new relevant data is uploaded"""

from datetime import datetime, timedelta, timezone

from botocore.client import BaseClient

from connections import get_bucket_connection


TIME_NOW = datetime.now(timezone.utc)


def get_items_in_buckets(s_three: BaseClient, bucket_name: str) -> list[tuple[str]]:
    """Function that finds the list of all items in the bucket"""
    return [(obj["Key"],obj["LastModified"]) for obj
            in s_three.list_objects(Bucket=bucket_name)["Contents"]]


def download_new_files(s_three: BaseClient, bucket_name: str, files: list[tuple[str]]) -> None:
    """Downloading relevant data from the past 3 hrs"""
    for file in files:
        time = TIME_NOW - timedelta(hours=3)
        if file[0][0:14] == "trucks/2023-8/" and file[1] > time:
            time = "-".join([str(TIME_NOW.day),str(TIME_NOW.hour),str(TIME_NOW.minute)])
            s_three.download_file(bucket_name, file[0], f"./data/{time}{file[0].split('/')[-1]}")


if __name__ == "__main__":
    aws_s_three = get_bucket_connection()

    all_items = get_items_in_buckets(aws_s_three, "sigma-resources-truck")
    download_new_files(aws_s_three, "sigma-resources-truck", all_items)
