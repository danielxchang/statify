from dataworkers.extensionparsers.csv_parser import CsvParser
from dataworkers.statisticians.basketball import BasketballStatistician

class DataProcessor:
    def __init__(self, sport = "basketball", file_type = 'csv'):
        self.__file_parser = self.__instantiate_file_parser(file_type)
        self.__statistician = self.____instantiate_statistician(sport)

    def __instantiate_file_parser(self, file_type):
        if file_type == 'csv':
            return CsvParser()

    def ____instantiate_statistician(self, sport):
        if sport == 'basketball':
            return BasketballStatistician(sport)

    def read_data(self, uploaded):
        self.__data = {key: self.__file_parser.read_data(file_path) for key, file_path in uploaded.items()}

    def translate_data(self):
        return self.__statistician.process_data(self.__data)

def read_data(data):
    for key, data_list in data.items():
        print(f'{key}: {len(data_list)} Records')
        for item in data_list:
            print(item)
        print('-----------------------DONE READING-----------------------')

def apply_test():
    uploaded = {
        'roster': 'csv-files/pbp_test copy.csv',
        'pbp': 'csv-files/rosters_test copy.csv'
    }
    dp = DataProcessor()
    data = dp.retrieve_data(uploaded)
    read_data(data)

if __name__ == "__main__":
    apply_test()