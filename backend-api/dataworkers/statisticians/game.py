class Game:
    def __init__(self):
        self.__teams = []
        self.__play_by_play = []
        self.__current_lineups = {}

    def start_game(self, teams, n_periods, period_length):
        self.__last_play_time = (1, period_length, 0)
        self.__n_periods = n_periods
        self.__period_length = period_length
        for team in teams:
            self.__teams.append(team)
    
    def add_play(self, period, time, team, play_string, latest_score):
        play = {
            "score": latest_score,
            "period": period,
            "time": time,
            "team": team,
            "description": play_string
        }
        self.__play_by_play.append(play)

    def connect_lineup(self, team, new_lineup):
        self.__current_lineups[team] = new_lineup
    
    def get_playtime_since_last_play(self, current_play_time):
        time_elapsed = self.tally_time_played(current_play_time)
        self.__last_play_time = current_play_time

        players_played = []
        for lineup in self.__current_lineups.values():
            players_played.extend(list(lineup))
        return players_played, time_elapsed

    def tally_time_played(self, latest_play_time):
        latest = self.calc_absolute_time(*latest_play_time)
        previous = self.calc_absolute_time(*self.__last_play_time)
        minutes = (latest - previous) // 60
        seconds = (latest - previous) % 60
        return (minutes, seconds)

    def calc_absolute_time(self, curr_period, curr_min_left, curr_sec_left):
        period_amt = ((curr_period - 1) * self.__period_length) * 60
        min_amt = (self.__period_length - curr_min_left) * 60
        return period_amt + min_amt - curr_sec_left

    def get_teams(self):
        return self.__teams
    
    def set_game_id(self, id):
        self.game_id = id

    def get_game_id(self):
        return self.game_id

    def get_pbp(self):
        return self.__play_by_play

    def end_game(self):
        final_pbp = self.get_pbp()
        final_result = {
            'final_score': final_pbp[-1]['score'],
            'pbp': final_pbp
        }
        return final_result