class Game:
    def __init__(self):
        self.__teams = []
        self.__play_by_play = []
        self.__current_lineups = {}

    def start_game(self, teams, n_periods, period_length):
        self.__last_play_time = (1, period_length)
        self.__n_periods = n_periods
        self.__period_length = period_length
        for team in teams:
            self.__teams.append(team)
    
    def add_play(self, period, time, team, play_string, latest_score):
        play = {
            "score'": latest_score,
            "period": period,
            "time": time,
            "team": team,
            "description": play_string
        }
        self.__play_by_play.append(play)

    def connect_lineup(self, team, new_lineup):
        self.__current_lineups[team] = new_lineup
    
    def get_playtime_since_last_play(self, current_period, current_period_duration_left):
        time_elapsed = self.tally_time_played(current_period, current_period_duration_left)
        self.__last_play_time = (current_period, current_period_duration_left)

        players_played = []
        for lineup in self.__current_lineups.values():
            players_played.extend(lineup)
        return players_played, time_elapsed

    def tally_time_played(self, current_period, current_period_duration_left):
        latest = self.calc_absolute_time(current_period, current_period_duration_left)
        previous = self.calc_absolute_time(*self.__last_play_time)
        minutes = (latest - previous) // 60
        seconds = (latest - previous) % 60
        return (minutes, seconds)

    def calc_absolute_time(self, curr_period, curr_min_left, curr_sec_left):
        period_amt = ((curr_period - 1) * self.__period_length) * 60
        min_amt = (self.__period_length - curr_min_left) * 60
        second_amt = 60 - curr_sec_left
        return period_amt + min_amt + second_amt

    def get_teams(self):
        return self.__teams
    
    def set_game_id(self, id):
        self.game_id = id

    def get_game_id(self):
        return self.game_id

    def get_pbp(self):
        return self.__play_by_play

    def end_game(self, final_score):
        final_result = {
            'score': final_score,
            'pbp': self.get_pbp()
        }
        return final_result