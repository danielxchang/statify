from pprint import pprint

from dataworkers.statisticians.statistician import Statistician

# REMOVE LATER
player_keys = ['player id', 'jersey #', 'team', 'full name', 'email', 'position', 'starting?']
pbp_keys = ['play-type', 'quarter', 'minute', 'seconds', 'shooter', 'shot type', 'made shot?', 'assist?', 'assister', 'shooting foul?', 'fouler', 'rebounder', 'block?', 'blocker', 'turnover committer', 'steal?', 'stealer', 'non-shooting fouler', 'subbing in', 'subbing out', 'timeout?', 'timeout team', 'quarter end']

class BasketballStatistician(Statistician):
    basketball_sport_id = 1

    def __init__(self):
        super().__init__()
        
    def process_data(self, data):
        players = data['roster']
        pbp = data['pbp']
        self.init_teams(players)
        self.process_rosters(players)
        # self.process_play_by_play(pbp)
        return self.finalize_data({'box-score': 'BOX', 'team-stats': 'TEAM'})

    def process_rosters(self, players):
        roster_map = {}
        for team in self.game.get_teams():
            team_entry = {
                'team_name': team,
                'league_id': None,
                'sport_id': self.basketball_sport_id
            }
            team_columns = [col for col in self.db_columns['teams'] if team_entry[col]]
            team_values = [[f'"{team_entry[col]}"' for col in self.db_columns['teams'] if team_entry[col]]]

            team_insert_args = {
                'table_name': 'teams', 
                'columns': team_columns,
                'values_list': team_values
            }
            team_insert_id = self.query_database('INSERT_INTO', team_insert_args)
            roster_map[team] = {'insert_id': team_insert_id, "players": {}, "starters": []}

        for player in players:
            player_team = player['team']
            names = player['full name'].split(' ')

            user_entry = {
                'first_name': names[0],
                'middle_name': ' '.join(names[1:-1]) if len(names) > 2 else None,
                'last_name': names[-1],
                'email': player['email'],
                'password': None
            }
            user_columns = [col for col in self.db_columns['users'] if user_entry[col]]
            user_values = [[f'"{user_entry[col]}"' for col in self.db_columns['users'] if user_entry[col]]]
            user_insert_args = {
                'table_name': 'users', 
                'columns': user_columns,
                'values_list': user_values
            }
            user_insert_id = self.query_database('INSERT_INTO', user_insert_args)

            player_columns = self.db_columns['players']
            player_values = [[f"{user_insert_id}", f"{roster_map[player_team]['insert_id']}", f"'{player['position']}'"]]
            player_insert_args = {
                'table_name': 'players', 
                'columns': player_columns,
                'values_list': player_values
            }
            player_insert_id = self.query_database('INSERT_INTO', player_insert_args)

            player_id = player['player id']
            roster_map[player_team]['players'][player_id] = player_insert_id
            if player['starting?']:
                roster_map[player_team]['starters'].append(player_id)
        pprint(roster_map)

    # NEXT
    def process_play_by_play(self, pbp):
        pbp_props = list(pbp[0].keys())
        for play in pbp:
            # INSERT INTO Query player data into players table of MySQL db
            pprint(play)

    def process_play(self, play):
        if play['play-type'].lower() == 'shooting':
            self.process_scoring(play)

    def process_scoring(self, play):
        # shooter, shot type, made shot?, assist?, assister, shooting foul, fouler, rebounder, # block? blocker
        pass

    def process_turnover(self, play):
        pass

    def process_non_shooting_foul(self, play):
        pass

    def process_sub(self, play):
        pass

    def stoppage(self, play):
        pass