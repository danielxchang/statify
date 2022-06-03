import pandas as pd
import numpy as np
from pprint import pprint
import re

# Models one unit of player/play data
class DataItem:
    def __init__(self, keys):
        self.item = {key: None for key in keys}

    def populate_item(self, record):
        for key in self.item:
            self.item[key] = record[key]

    def print_item(self):
        pprint(self.item)

"""
Models a data extractor that reads data 
from csv and converts to list of DataItems
"""
class DataExtractor:
    def read_data(self, file_path):
        df = self.clean_dataframe(file_path)
        headers = df.columns
        data = []

        # Converts the csv record data into DataItems
        for i in range(len(df)):
            item = DataItem(headers)
            item.populate_item(df.iloc[i])
            data.append(item)
        return data

    def clean_dataframe(self, path):
        # Drop any empty rows before headers
        df = pd.read_csv(path, skip_blank_lines=True)
        df.dropna(how="all", inplace=True)

        # Checks that columns are set to proper headers
        if re.search("Unnamed", df.columns[0]):
            df = self.set_first_row_as_headers(df) 
            df.to_csv(path, index=False)
            df = pd.read_csv(path)

        # Replaces any "nan" values with None
        df = df.replace({np.nan:None})
        return df

    def set_first_row_as_headers(self, df):
        df.columns = df.iloc[0]
        df = df[1:]
        return df