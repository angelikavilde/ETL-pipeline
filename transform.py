"""Code that merges parquet files and adds an index column"""

from os import listdir, remove

import pandas as pd


def combine_transaction_data_files(files: list[str]) -> None:
    """Loads and combines csv files"""
    data_frame = pd.DataFrame()
    for file in files:
        data_frame = pd.read_csv(file)
        truck_id = int(file.split("_")[1][-1])
        data_frame.insert(0,"truck_id",[truck_id for _ in range(len(data_frame.index))])
        data_frame = pd.concat([data_frame, data_frame], axis=0)
    data_frame.to_csv('./data/data_combined.csv', index=False)


if __name__ == "__main__":
    file_paths = ["data/" + file for file in listdir("data")]
    combine_transaction_data_files(file_paths)
    for filepath in file_paths:
        remove(filepath)
