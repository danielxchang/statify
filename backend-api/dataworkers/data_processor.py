from dataworkers.extensionparsers.csv_parser import CsvParser
from dataworkers.statisticians.basketball import BasketballStatistician

class DataProcessor:
    def __init__(self, sport = "basketball", file_type = None):
        if file_type:
            self.__file_parser = self.__instantiate_file_parser(file_type)
        self.__statistician = self.____instantiate_statistician(sport)

    def __instantiate_file_parser(self, file_type):
        if file_type == 'csv':
            return CsvParser()

    def ____instantiate_statistician(self, sport):
        if sport == 'basketball':
            return BasketballStatistician(sport)

    def read_data(self, uploaded):
        data = {key: self.__file_parser.read_data(file_path) for key, file_path in uploaded.items()}
        self.__statistician.receive_data(data)

    def translate_data(self):
        stat_data = self.__statistician.process_data()
        return self.check_data_validity(stat_data)
    
    def retrieve_data(self, game_id):
        stat_data = self.__statistician.get_game_data(game_id)
        return self.check_data_validity(stat_data)

    def get_all_games(self):
        return self.__statistician.get_all_game_recaps()

    def check_data_validity(self, data):
        for category in ['box_score', 'team_stats', 'pbp', 'teams']:
            if category not in data or not data[category]:
                return False
        return data

def read_test_data(data):
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
    read_test_data(data)

if __name__ == "__main__":
    apply_test()