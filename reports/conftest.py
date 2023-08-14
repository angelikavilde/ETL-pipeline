"""File with additions for testing"""

import pytest
import pandas as pd
from pandas import DataFrame

@pytest.fixture
def data() -> DataFrame:
    """Returns a dataframe for tests"""
    cols = ["sum_total", "truck_name"]
    test_data = [[2,"test"],[1,"test2"]]
    return pd.DataFrame(data=test_data,columns=cols, index=["1","2"])


@pytest.fixture
def transactions() -> DataFrame:
    """Returns a dataframe for tests"""
    cols = ["number_of_transactions", "mean", "median", "sum_total", "truck_name"]
    test_data = [[2,5,5,6, "test1"],[1,5,3,6,"test2"]]
    return pd.DataFrame(data=test_data,columns=cols, index=["1","2"])


@pytest.fixture
def returned_transactions(transactions) -> DataFrame:
    """Returns formatted cursor returned dataframe"""
    columns = ['sum_total',"number_of_transactions","mean","median"]
    transactions[columns] = transactions[columns].astype(float)
    transactions.set_index(["truck_name"])
    return transactions
