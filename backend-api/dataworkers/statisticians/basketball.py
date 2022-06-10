from pprint import pprint
from collections import deque
from dataworkers.statisticians.statistician import Statistician

# REMOVE LATER
player_keys = ['player id', 'jersey #', 'team', 'full name', 'email', 'position', 'starting?']
pbp_keys = ['play-type', 'quarter', 'minute', 'seconds', 'shooter', 'shot type', 'made shot?', 'assist?', 'assister', 'shooting foul?', 'fouler', 'rebounder', 'block?', 'blocker', 'turnover committer', 'steal?', 'stealer', 'non-shooting fouler', 'subbing in', 'subbing out', 'timeout?', 'timeout team', 'quarter end']

class BasketballStatistician(Statistician):
    gamelog_table = "basketball_gamelogs"
    periods = 4
    period_length = 12
    point_values = {
        'Free Throw': 1,
        '2-Pointer': 2,
        '3-Pointer': 3
    }
    stat_events = ['shot', 'rebound', 'steal', 'block', 'turnover', 'foul', 'sub']

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
            pprint(play_map['play_string'])

    def process_shooting(self, play):
        play_map = self.process_shot(play)
        self.play_queue.append(play_map)
        made_shot = play["made shot?"]

        if made_shot and play['assist?']:
            self.process_assist(play['assister'], play_map)
        
        if play['shooting foul?']:
            self.process_foul(play['fouler'], play_map)
        elif not made_shot:
            if play['block?']:
                self.process_block(play['blocker'], play_map)
            self.process_rebound(play['rebounder'], play_map['team'])

    def process_shot(self, play):
        shooter_input_id = play['shooter']
        shooter_gamelog_id = self.get_player_attribute(shooter_input_id, 'gamelog_id')
        shooter_team = self.get_team(shooter_input_id)
        shooter_name = self.get_player_attribute(shooter_input_id, 'full_name')
        point_value = self.point_values[play["shot type"]]
        made_shot = play["made shot?"]
        play_string = f"{shooter_name} {'makes' if made_shot else 'misses'} {point_value}-point shot"

        return {
            'type': 'shot',
            'gamelog_id': shooter_gamelog_id,
            'player_name': shooter_name,
            'team': shooter_team,
            'play_string': play_string,
            'made_shot': made_shot,
            'points': point_value
        }

    def process_foul(self, fouler_input_id, shot_play_map = False):
        fouler_id = self.get_player_attribute(fouler_input_id, 'gamelog_id')
        fouler_name = self.get_player_attribute(fouler_input_id, 'full_name')
        fouler_team = self.get_team(fouler_input_id)
        foul_string = f"{fouler_name} {'shooting' if shot_play_map else 'personal'} foul"

        new_play_map = {
            'type': 'foul',
            'gamelog_id': fouler_id,
            'team': fouler_team,
            'play_string': foul_string
        }
        
        if shot_play_map and not shot_play_map['made_shot']:
            shot_play_map.clear()
            for key in new_play_map:
                shot_play_map[key] = new_play_map[key]
        else:
            self.play_queue.append(new_play_map)

    def process_assist(self, assister_input_id, play_map):
        assister_gamelog_id = self.get_player_attribute(assister_input_id, 'gamelog_id')
        assister_name = self.get_player_attribute(assister_input_id, 'full_name')
        play_map['play_string'] += f' ({assister_name} assists)'
        play_map['assister_gamelog_id'] = assister_gamelog_id

    def process_rebound(self, rebounder_input_id, shooting_team):
        rebounder_gamelog_id = self.get_player_attribute(rebounder_input_id, 'gamelog_id')
        rebounder_team = self.get_team(rebounder_input_id)
        rebounder_name = self.get_player_attribute(rebounder_input_id, 'full_name')
        rebound_type = 'offensive' if shooting_team == rebounder_team else 'defensive'
        play_string = f"{rebounder_name} {rebound_type} rebound"
       
        new_play_map = {
            'type': 'rebound',
            'rebound_type': rebound_type,
            'gamelog_id': rebounder_gamelog_id,
            'team': rebounder_team,
            'play_string': play_string
        }
        self.play_queue.append(new_play_map)

    def process_block(self, blocker_input_id, play_map):
        blocker_id = self.get_player_attribute(blocker_input_id, 'gamelog_id')
        blocker_name = self.get_player_attribute(blocker_input_id, 'full_name')
        block_string = f"{blocker_name} blocks {play_map['player_name']}'s {play_map['points']}-point shot"
        play_map['blocker_gamelog_id'] = blocker_id
        play_map['play_string'] = block_string

    def process_turnover(self, play):
        turnover_input_id = play['turnover committer']
        turnover_team = self.get_team(turnover_input_id)
        turnover_id = self.get_player_attribute(turnover_input_id, 'gamelog_id')
        turnover_name = self.get_player_attribute(turnover_input_id, 'full_name')
        play_string = f"{turnover_name} turnover"

        play_map = {
            'type': 'turnover',
            'gamelog_id': turnover_id,
            'team': turnover_team,
            'play_string': play_string
        }

        if play['steal?']: 
            stealer_input_id = play['stealer']
            stealer_id = self.get_player_attribute(stealer_input_id, 'gamelog_id')
            stealer_name = self.get_player_attribute(stealer_input_id, 'full_name')
            play_map["stealer_id"] = stealer_id
            play_map["play_string"] += f" ({stealer_name} steals)"
        
        self.play_queue.append(play_map)

    def process_non_shooting_foul(self, play):
        self.process_foul(play['non-shooting fouler'])

    def process_sub(self, play):
        sub_in_input_id = play['subbing in']
        sub_in_team = self.get_team(sub_in_input_id)
        sub_in_name = self.get_player_attribute(sub_in_input_id, 'full_name')

        sub_out_input_id = play['subbing out']
        sub_out_name = self.get_player_attribute(sub_out_input_id, 'full_name')
        play_string = f"{sub_in_name} enters the game for {sub_out_name}"

        play_map = {
            'type': 'substitution',
            'team': sub_in_team,
            'play_string': play_string
        }
        
        self.play_queue.append(play_map)

    # THIS NEXT
    def process_stoppage(self, play):
        pass
        
    def get_player_attribute(self, player_input_id, attribute):
        player_map = self.roster_map[self.get_team(player_input_id)]['players'][player_input_id]
        return player_map[attribute]

    def get_team(self, player_input_id):
        return player_input_id.split('-')[-1].lstrip()
