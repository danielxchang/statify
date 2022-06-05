import pandas as pd
import numpy as np
from pprint import pprint
import re

"""
Models a data extractor that reads data 
from csv and converts to list of Python dictionaries
"""
class CsvParser:
    def read_data(self, file_path):
        df = self.clean_dataframe(file_path)
        headers = df.columns
        data = []
        for i in range(len(df)):
            item = {}
            for header in headers:
                item[header.lower()] = df.iloc[i][header]
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