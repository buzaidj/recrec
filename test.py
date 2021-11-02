from unittest import TestCase
from load_data import dataframe_of_json
import pandas as pd


class TestLoadData(TestCase):
    def test_load_data_from_json(self):
        data = """[
            {
                "x": 5,
                "y": 10
            },
            {
                "x": 2,
                "y": 23
            }
        ]"""
        dataframe = dataframe_of_json(data)
        self.assertTrue(pd.DataFrame.equals(dataframe, pd.DataFrame(
            [{'x': 5, 'y': 10}, {'x': 2, 'y': 23}])))
