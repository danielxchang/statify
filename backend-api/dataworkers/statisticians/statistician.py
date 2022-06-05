from dataworkers.statisticians.game import Game

class Statistician:
    def __init__(self):
        self.game = Game()
        
    def init_teams(self, players):
        teams = set()
        for player in players:
            teams.add(player['team'])
        self.game.start_game(teams)
    
    def finalize_data(self, query_data):
        final_data = self.game.end_game()
        for key, value in query_data.items():
            final_data[key] = value
        return final_data