from data_extractor import DataExtractor

class PlayByPlay:
    def __init__(self, sport = "basketball"):
        self.extractor = DataExtractor()
        self.plays = None
        self.players = None
        self.sport = sport

    def retrieve_data(self, roster_csv, pbp_csv):
        self.plays = self.extractor.read_data(pbp_csv)
        self.players = self.extractor.read_data(roster_csv)

def apply_test():
    test_pbp_file = 'csv-files/pbp_test copy.csv'
    test_rosters_file = 'csv-files/rosters_test copy.csv'
    pbp = PlayByPlay()
    pbp.retrieve_data(test_rosters_file, test_pbp_file)
    print('PLAYERS')
    for player in pbp.players:
        player.print_item()
    
    print('-----------------------')
    print('PLAYS')
    for play in pbp.plays:
        play.print_item()

if __name__ == "__main__":
    apply_test()