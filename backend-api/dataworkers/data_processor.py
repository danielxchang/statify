from dataworkers.csv_parser import CsvParser

class DataProcessor:
    def __init__(self, sport = "basketball", file_type = 'csv'):
        self.__parser = None
        self.__sport = sport
        self.__parse_files(file_type)

    def __parse_files(self, file_type):
        if file_type == 'csv':
            self.__parser = CsvParser()

    def retrieve_data(self, uploaded):
        data = {key: self.__parser.read_data(file_path) for key, file_path in uploaded.items()}
        return data

def read_data(data):
    for key, data_list in data.items():
        print(f'{key}: {len(data_list)} Records')
        for item in data_list:
            item.print_item()
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