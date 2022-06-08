from dataworkers.statisticians.game import Game
from database.database import *

class Statistician:
    db_name = 'statify'
    db_columns = {
        'users': ['first_name', 'middle_name', 'last_name', 'email', 'password'],
        'teams': ['team_name', 'league_id', 'sport_id'],
        'players': ['user_id', 'team_id', 'position']
    }

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

    def query_database(self, query_type, query_args):
        use_database(self.db_name)
        if query_type == 'INSERT_INTO':
            return self.insert(query_args)

    def insert(self, query_args):
        insert_into_query(query_args['table_name'], query_args['columns'], query_args['values_list'])
        return get_last_insert_id()