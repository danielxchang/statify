from dataworkers.statisticians.game import Game
from database.database import *
from database.setup_db import get_db_map

class Statistician:
    def __init__(self, sport):
        self.game = Game()
        self.sport = sport
        self.init_db_map()
        self.init_sport_id()
        
    def init_teams(self, players):
        teams = set()
        for player in players:
            teams.add(player['team'])
        self.game.start_game(teams)

    def init_db_map(self):
        self.db_name, self.db_columns = get_db_map(self.sport)

    def init_sport_id(self):
        select_query_args = {
            'SELECT': ['id'],
            "FROM": 'sports',
            "WHERE": f"sport_name = '{self.sport}'"
        }
        query_data = self.query_database('SELECT', select_query_args)
        self.sport_id = query_data['records'][0][0] if query_data['records'] else None

    def init_roster_map(self):
        self.roster_map = {
            team: {
                'team_id': None,
                "players": {},
                "starters": []
            } for team in self.game.get_teams()
        }

    def finalize_data(self, query_data):
        final_data = self.game.end_game()
        for key, value in query_data.items():
            final_data[key] = value
        return final_data

    def query_database(self, query_type, query_args):
        use_database(self.db_name)
        if query_type == 'INSERT_INTO':
            return self.insert(query_args)
        if query_type == 'SELECT':
            return self.select(query_args)
        if query_type == 'UPDATE':
            return self.update(query_args)

    def insert(self, query_args):
        table_name = query_args['table_name']
        columns = query_args['columns']
        values_list = query_args['values_list']
        response = insert_into_query(table_name, columns, values_list)
        print(response[1])
        # print(f'Inserted {len(values_list)} record(s) into {table_name}')
        return get_last_insert_id()

    def select(self, query_args):
        response = select_query(query_args)
        print(response[1])
        return get_last_query()

    def update(self, query_args):
        # TO DO
        return

    def does_record_exist(self, select_query_args):
        match_records = self.query_database('SELECT', select_query_args)['records']
        return match_records[0][0] if len(match_records) else False
    
    def format_input(self, input):
        return f'"{input}"' if type(input) == str else str(input)

    def format_input_list(self, input_list, join_sep = ', '):
        return join_sep.join([self.format_input(input_item) for input_item in input_list])

    def process_users(self, players):
        returning_user_ids = []
        for player in players:
            player_team = player['team']
            names = player['full name'].split(' ')
            email = player['email']

            user_select_query_args = {
                'SELECT': ['id'],
                "FROM": 'users',
                "WHERE": f"email = '{email}'"
            }
            user_id = self.does_record_exist(user_select_query_args)
            if user_id:
                returning_user_ids.append(user_id)
            else:
                user_entry = {
                    'first_name': names[0],
                    'middle_name': ' '.join(names[1:-1]) if len(names) > 2 else None,
                    'last_name': names[-1],
                    'email': email
                }
                user_columns = [
                    col for col in self.db_columns['users'] 
                    if col in user_entry and user_entry[col]
                ]
                
                user_values = [[self.format_input(user_entry[col]) for col in user_columns]]
                user_insert_args = {
                    'table_name': 'users', 
                    'columns': user_columns,
                    'values_list': user_values
                }
                user_id = self.query_database('INSERT_INTO', user_insert_args)
            
            p_input_id = player['player id']
            self.roster_map[player_team]['players'][p_input_id] = {"user_id": user_id}
            if player['starting?']:
                self.roster_map[player_team]['starters'].append(p_input_id)
        return returning_user_ids

    def process_teams(self, returning_user_ids):
        self.find_existing_teams(returning_user_ids)
        self.add_new_teams()

    def find_existing_teams(self, existing_user_ids):
        if not existing_user_ids:
            return 
            
        user_ids_string = self.format_input_list(existing_user_ids)
        team_names_string = self.format_input_list(self.roster_map)
        where_condition = f'user_id IN ({user_ids_string}) AND team_name IN ({team_names_string})'
        join_select_args = {
            'SELECT': ['team_id', 'team_name', 'COUNT(team_id) AS player_count'],
            "FROM": 'players',
            "JOIN": [
                ["INNER", 'teams', 'teams.id = players.team_id']
            ],
            "WHERE": where_condition,
            "GROUP BY": ['team_id'],
            "ORDER BY": ["player_count"],
            "LIMIT": {
                "count": len(self.roster_map),
                "offset": 0
            },
        }
        query_data = self.query_database('SELECT', join_select_args)
        print(query_data)
        if query_data['records']:
            for team_id, team_name, _ in query_data['records']:
                self.roster_map[team_name]['team_id'] = team_id

    def add_new_teams(self):
        for team in self.roster_map:
            if not self.roster_map[team]['team_id']:
                team_entry = {
                    'team_name': team,
                    'league_id': None,
                    'sport_id': self.sport_id
                }
                team_columns = [
                    col for col in self.db_columns['teams'] 
                    if col in team_entry and team_entry[col]
                ]
                team_values = [[self.format_input(team_entry[col]) for col in team_columns]]

                team_insert_args = {
                    'table_name': 'teams', 
                    'columns': team_columns,
                    'values_list': team_values
                }
                team_id = self.query_database('INSERT_INTO', team_insert_args)
                self.roster_map[team]['team_id'] = team_id
    
    def process_players(self, players):
        for player in players:
            player_team = player['team']
            player_team_id = self.roster_map[player_team]['team_id']
            p_input_id = player['player id']
            user_id = self.roster_map[player_team]['players'][p_input_id]['user_id']
            player_select_query_args = {
                'SELECT': ['id'],
                "FROM": 'players',
                "WHERE": f"user_id = {user_id} AND team_id = {player_team_id}"
            }
            player_id = self.does_record_exist(player_select_query_args)
            if not player_id:
                player_entry = {
                    "user_id": user_id,
                    "team_id": player_team_id
                }
                player_columns = [
                    col for col in self.db_columns['players'] 
                    if col in player_entry and player_entry[col]
                ]
                
                player_values = [[self.format_input(player_entry[col]) for col in player_columns]]
                player_insert_args = {
                    'table_name': 'players', 
                    'columns': player_columns,
                    'values_list': player_values
                }
                player_id = self.query_database('INSERT_INTO', player_insert_args)

            self.roster_map[player_team]['players'][p_input_id]['player_id'] = player_id