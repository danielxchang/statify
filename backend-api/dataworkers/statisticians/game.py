class Play:
    def __init__(self, time, team, string, score):
        self.time = time
        self.team = team
        self.string = string
        self.score = score

class Game:
    def __init__(self):
        self.__teams = []
        self.__score = {}
        self.__play_by_play = []

    def start_game(self, teams, starting_score = 0):
        for team in teams:
            self.__teams.append(team)
            self.__score[team] = starting_score
    
    def add_play(self, time, team, play_string, is_scoring_play = False, points_scored = 0):
        if is_scoring_play:
            self.__update_score(team, points_scored)
        self.__play_by_play.append(Play(time, team, play_string, self.__score))

    def get_teams(self):
        return self.__teams

    def end_game(self):
        final_result = {
            'score': self.__score,
            'pbp': self.__play_by_play
        }
        return final_result

    def __update_score(self, scoring_team, amount):
        self.__score[scoring_team] += amount
