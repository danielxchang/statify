from pprint import pprint
from collections import deque
from dataworkers.statisticians.statistician import Statistician

# REMOVE LATER
player_keys = ['player id', 'jersey #', 'team', 'full name', 'email', 'position', 'starting?']
pbp_keys = ['play-type', 'quarter', 'minute', 'seconds', 'shooter', 'shot type', 'made shot?', 'assist?', 'assister', 'shooting foul?', 'fouler', 'rebounder', 'block?', 'blocker', 'turnover committer', 'steal?', 'stealer', 'non-shooting fouler', 'subbing in', 'subbing out', 'timeout?', 'timeout team', 'quarter end']

class BasketballStatistician(Statistician):
    gamelog_table = "basketball_gamelogs"
    period_strings = {
        1: '1st',
        2: '2nd',
        3: '3rd',
        4: '4th'
    }
    periods = 4
    period_length = 12
    point_values = {
        'Free Throw': 1,
        '2-Pointer': 2,
        '3-Pointer': 3
    }
    shot_columns_start = {
        1: 'free_throw',
        2: 'two_point',
        3: 'three_point'
    }
    
    def __init__(self, sport):
        super().__init__(sport)
        self.init_method_map()
        self.play_queue = deque()

    def init_method_map(self):
        self.play_type_method_map = {
            'shooting': self.process_shooting,
            'non-shooting foul': self.process_non_shooting_foul,
            'turnover': self.process_turnover,
            'substitution': self.process_sub,
            'stoppage': self.process_stoppage
        }

    def process_play(self, play):
        play_type = play['play-type'].lower()

        self.play_type_method_map[play_type](play)
        while self.play_queue:
            play_map = self.play_queue.popleft()
            self.accumulate_minutes(play_map)
            stat_events = self.convert_to_stat(play_map)
            self.tally_stats(stat_events)
            self.game.add_play(play_map['quarter'], f"{play_map['minute']}:{play_map['second']}", play_map['team'], play_map['play_string'], self.get_current_score())

    def accumulate_minutes(self, play_map):
        curr_play_time = (play_map['quarter'], play_map['minute'], play_map['second'])
        played, time_played = self.game.get_playtime_since_last_play(curr_play_time)
        minutes_played, seconds_played = time_played
        minute_changes = {
            gamelog_id: {
                "minutes_played": f"{minutes_played} + FLOOR((seconds_played + {seconds_played}) / 60)",
                "seconds_played": f"MOD(seconds_played + {seconds_played}, 60) - seconds_played"
            } 
            for gamelog_id in played
        }
        self.tally_stats(minute_changes)

    def convert_to_stat(self, play_map):
        stat_events = {}
        if play_map['type'] == 'shot':
            points = play_map['points']
            shot_type = self.shot_columns_start[points]
            stat_events[play_map['gamelog_id']] = {
                f"{shot_type}_makes": 1 if play_map['made_shot'] else 0,
                f"{shot_type}_attempts": 1,
                "points": points if play_map['made_shot'] else 0 
            }
            if 'assister_gamelog_id' in play_map:
                self.add_singular_stat_event(play_map, stat_events, 'assists', 'assister_gamelog_id')
            if 'blocker_gamelog_id' in play_map:
                self.add_singular_stat_event(play_map, stat_events, 'blocks', 'blocker_gamelog_id')
        elif play_map['type'] == 'rebound':
            self.add_singular_stat_event(play_map, stat_events, f"{play_map['rebound_type']}_rebounds")
        elif play_map['type'] == 'foul':
            self.add_singular_stat_event(play_map, stat_events, 'fouls')
        elif play_map['type'] == 'turnover':
            self.add_singular_stat_event(play_map, stat_events, 'turnovers')
            if 'stealer_gamelog_id' in play_map:
                self.add_singular_stat_event(play_map, stat_events, 'steals', 'stealer_gamelog_id')
        elif play_map['type'] == 'substitution':
            lineups = self.roster_map[play_map['team']]['in_game']
            lineups.remove(play_map['out'])
            lineups.add(play_map['in'])

        return stat_events
    
    def add_singular_stat_event(self, play_map, stat_events, stat_key, gamelog_id = 'gamelog_id'):
        stat_events[play_map[gamelog_id]] = {stat_key: 1}

    def tally_stats(self, stat_events):
        for gamelog_id, stat_event in stat_events.items():
            set_assignments = []
            for stat_column, increment_value in stat_event.items():
                if stat_column == 'points' and increment_value > 0:
                    self.update_score(gamelog_id, increment_value)
                set_assignments.append(f"{stat_column} = {stat_column} + {increment_value}")
            update_args = {
                'table_name': self.gamelog_table,
                'set_assignments': set_assignments,
                'where_condition': f'id = {gamelog_id}'
            }
            self.data_clerk.update(update_args)

    def update_score(self, scorer_gamelog_id, points_scored):
        team_number = self.get_team_number(scorer_gamelog_id)
        update_column = f"team{team_number}_score"
        update_args = {
            'table_name': "games",
            'set_assignments': [f"{update_column} = {update_column} + {points_scored}"],
            'where_condition': f'id = {self.game.get_game_id()}'
        }
        self.data_clerk.update(update_args)

    def process_shooting(self, play):
        play_map = self.process_shot(play)
        self.add_moment_props(play, play_map)
        self.play_queue.append(play_map)
        made_shot = play["made shot?"]

        if made_shot and play['assist?']:
            self.process_assist(play, play_map)
        
        if play['shooting foul?']:
            self.process_foul(play, play_map)
        elif not made_shot:
            if play['block?']:
                self.process_block(play, play_map)
            if play['rebounder']:
                self.process_rebound(play, play_map['team'])

    def process_shot(self, play):
        shooter_id, shooter_team, shooter_name = self.get_player_info(play['shooter'])
        point_value = self.point_values[play["shot type"]]

        return {
            'type': 'shot',
            'gamelog_id': shooter_id,
            'player_name': shooter_name,
            'team': shooter_team,
            'play_string':  f"{shooter_name} {'makes' if play['made shot?'] else 'misses'} {point_value}-point shot",
            'made_shot': play["made shot?"],
            'points': point_value
        }

    def process_foul(self, play, shot_play_map = False):
        fouler_input_id = play['fouler'] if shot_play_map else play['non-shooting fouler']
        fouler_id, fouler_team, fouler_name = self.get_player_info(fouler_input_id)

        new_play_map = {
            'type': 'foul',
            'gamelog_id': fouler_id,
            'team': fouler_team,
            'play_string': f"{fouler_name} {'shooting' if shot_play_map else 'personal'} foul"
        }
        self.add_moment_props(play, new_play_map)
        
        if shot_play_map and not shot_play_map['made_shot']:
            shot_play_map.clear()
            for key in new_play_map:
                shot_play_map[key] = new_play_map[key]
        else:
            self.play_queue.append(new_play_map)

    def process_assist(self, play, play_map):
        assister_input_id = play['assister']
        assister_id, _, assister_name = self.get_player_info(assister_input_id)
        play_map['play_string'] += f' ({assister_name} assists)'
        play_map['assister_gamelog_id'] = assister_id

    def process_rebound(self, play, shooting_team):
        rebounder_input_id = play['rebounder']
        rebounder_id, rebounder_team, rebounder_name = self.get_player_info(rebounder_input_id)
        rebound_type = 'offensive' if shooting_team == rebounder_team else 'defensive'
        new_play_map = {
            'type': 'rebound',
            'rebound_type': rebound_type,
            'gamelog_id': rebounder_id,
            'team': rebounder_team,
            'play_string': f"{rebounder_name} {rebound_type} rebound"
        }
        self.add_moment_props(play, new_play_map)
        self.play_queue.append(new_play_map)

    def process_block(self, play, play_map):
        blocker_input_id = play['blocker']
        blocker_id, _, blocker_name = self.get_player_info(blocker_input_id)
        play_map['blocker_gamelog_id'] = blocker_id
        play_map['play_string'] = f"{blocker_name} blocks {play_map['player_name']}'s {play_map['points']}-point shot"

    def process_turnover(self, play):
        turnover_id, turnover_team, turnover_name = self.get_player_info(play['turnover committer'])
        play_map = {
            'type': 'turnover',
            'gamelog_id': turnover_id,
            'team': turnover_team,
            'play_string': f"{turnover_name} turnover"
        }

        if play['steal?']: 
            stealer_id, _, stealer_name = self.get_player_info(play['stealer'])
            play_map["stealer_gamelog_id"] = stealer_id
            play_map["play_string"] += f" ({stealer_name} steals)"
        
        self.add_moment_props(play, play_map)
        self.play_queue.append(play_map)

    def process_non_shooting_foul(self, play):
        self.process_foul(play)

    def process_sub(self, play):
        sub_in_id, sub_in_team, sub_in_name = self.get_player_info(play['subbing in'])
        sub_out_id, _, sub_out_name = self.get_player_info(play['subbing out'])
        play_string = f"{sub_in_name} enters the game for {sub_out_name}"
        play_map = {
            'type': 'substitution',
            'team': sub_in_team,
            'play_string': play_string,
            'in': sub_in_id,
            'out': sub_out_id
        }
        self.add_moment_props(play, play_map)
        self.play_queue.append(play_map)

    def process_stoppage(self, play):
        if play['quarter end']:
            quarter = int(play['quarter'])
            play_string = f"End of the {self.period_strings[quarter]} Quarter"
        else:
            play_string = f"{play['timeout team']} timeout"

        play_map = {
            'type': 'stoppage',
            'team': play['timeout team'] if play['timeout?'] else None,
            'play_string': play_string
        }
        self.add_moment_props(play, play_map)
        self.play_queue.append(play_map)

    def add_moment_props(self, play, play_map):
        props = ['quarter', 'minute', 'second']
        for prop in props:
            play_map[prop] = int(play[prop]) if play[prop] else 0

    def get_player_attribute(self, player_input_id, attribute):
        player_map = self.roster_map[self.get_team(player_input_id)]['players'][player_input_id]
        return player_map[attribute]

    def get_team(self, player_input_id):
        return player_input_id.split('-')[-1].lstrip()

    def get_player_info(self, input_id):
        gamelog_id = self.get_player_attribute(input_id, 'gamelog_id')
        team = self.get_team(input_id)
        name = self.get_player_attribute(input_id, 'full_name')
        return gamelog_id, team, name
    
    def get_box_score(self):
        # Make MySQL SELECT QUERY TO GET ALL gamelogs
        """
        SELECT 
        CONCAT(users.first_name, ' ', users.last_name, ' ', position) AS player, 
        ROUND((minutes_played * 60 + seconds_played) / 60, 0) AS MIN,
        CONCAT(two_point_makes + three_point_makes, '-', two_point_attempts + three_point_attempts) AS FG,
        CONCAT(three_point_makes, '-', three_point_attempts) AS 3PT,
        CONCAT(free_throw_makes, '-', free_throw_attempts) AS FT,
        offensive_rebounds AS OREB,
        defensive_rebounds AS DREB,
        offensive_rebounds + defensive_rebounds AS REB,
        assists AS AST,
        steals AS STL,
        blocks AS BLK,
        turnovers AS "TO",
        fouls as PF,
        points AS PTS
        FROM basketball_gamelogs
        JOIN performances
            ON performances.gamelog_id = basketball_gamelogs.id
        JOIN players
            ON players.id = performances.player_id
        JOIN users
            ON users.id = players.user_id
        JOIN player_positions
            ON performances.player_position_id = player_positions.id
        JOIN positions
            ON player_positions.position_id = positions.id
        WHERE team_id = 1;
        """
        pass

    def get_team_stats(self):
        # Make MySQL SELECT QUERY TO GET ALL gamelogs
        '''
        SELECT 
        team_name AS team,
        CONCAT(
            SUM(two_point_makes + three_point_makes), 
            '-', 
            SUM(two_point_attempts + three_point_attempts)
        ) AS FG,
        ROUND(IFNULL(SUM(two_point_makes + three_point_makes) / SUM(two_point_attempts + three_point_attempts) * 100, 0), 1) AS "Field Goal %",
        CONCAT(
            SUM(three_point_makes), 
            '-', 
            SUM(three_point_attempts)
        ) AS 3PT,
        ROUND(IFNULL(SUM(three_point_makes) / SUM(three_point_attempts) * 100, 0), 1) AS "Three Point %",
        CONCAT(
            SUM(free_throw_makes),
            '-', 
            SUM(free_throw_attempts)
        ) AS FT,
        ROUND(IFNULL(SUM(free_throw_makes) / SUM(free_throw_attempts) * 100, 0), 1) AS "Free Throw %",
        SUM(offensive_rebounds) AS OREB,
        SUM(defensive_rebounds) AS DREB,
        SUM(offensive_rebounds) + SUM(defensive_rebounds) AS REB,
        SUM(assists) AS AST,
        SUM(steals) AS STL,
        SUM(blocks) AS BLK,
        SUM(turnovers) AS "TO",
        SUM(fouls) as PF,
        SUM(points) AS PTS
        FROM basketball_gamelogs
        JOIN performances
            ON performances.gamelog_id = basketball_gamelogs.id
        JOIN players
            ON players.id = performances.player_id
        JOIN users
            ON users.id = players.user_id
        JOIN player_positions
            ON performances.player_position_id = player_positions.id
        JOIN positions
            ON player_positions.position_id = positions.id
        JOIN teams
            ON players.team_id = teams.id
        GROUP BY team_id;
        '''
        pass