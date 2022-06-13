def get_join_args(gamelog_table):
    return [
        ["INNER", "performances", f"performances.gamelog_id = {gamelog_table}.id"],
        ["INNER", "players", "players.id = performances.player_id"],
        ["INNER", "users", "users.id = players.user_id"],
        ["INNER", "player_positions", "performances.player_position_id = player_positions.id"],
        ["INNER", "positions", "player_positions.position_id = positions.id"]
    ]

def get_select_args(sport, table_type):
    return select_args[sport][table_type]

pbp_select_columns = [
    'period', 
    'CONCAT(minute, ":", LPAD(second, 2, "0")) AS time',
    'team_name', 
    'play_string', 
    'score'
]

basketball_select_args = {
    'BOX_SCORE': [
        "CONCAT(users.first_name, ' ', users.last_name, ' ', position) AS player",
        "CAST(ROUND((minutes_played * 60 + seconds_played) / 60, 0) AS SIGNED) AS MIN",
        "CONCAT(two_point_makes + three_point_makes, '-', two_point_attempts + three_point_attempts) AS FG",
        "CONCAT(three_point_makes, '-', three_point_attempts) AS 3PT",
        "CONCAT(free_throw_makes, '-', free_throw_attempts) AS FT",
        "offensive_rebounds AS OREB",
        "defensive_rebounds AS DREB",
        "offensive_rebounds + defensive_rebounds AS REB",
        "assists AS AST",
        "steals AS STL",
        "blocks AS BLK",
        "turnovers AS 'TO'",
        "fouls AS PF",
        "points AS PTS"
    ],
    'TEAM_STATS': [
        "CAST(SUM(points) AS SIGNED) AS PTS",
        "CAST(CONCAT(SUM(two_point_makes + three_point_makes), '-', SUM(two_point_attempts + three_point_attempts)) AS CHAR) AS FG",
        "CONCAT(ROUND(IFNULL(SUM(two_point_makes + three_point_makes) / SUM(two_point_attempts + three_point_attempts) * 100, 0), 1), '%') AS 'Field Goal %'",
        "CAST(CONCAT(SUM(three_point_makes), '-', SUM(three_point_attempts)) AS CHAR) AS 3PT",
        "CONCAT(ROUND(IFNULL(SUM(three_point_makes) / SUM(three_point_attempts) * 100, 0), 1), '%') AS 'Three Point %'",
        "CAST(CONCAT(SUM(free_throw_makes),'-', SUM(free_throw_attempts)) AS CHAR) AS FT",
        "CONCAT(ROUND(IFNULL(SUM(free_throw_makes) / SUM(free_throw_attempts) * 100, 0), 1), '%') AS 'Free Throw %'",
        "CAST(SUM(offensive_rebounds) AS SIGNED) AS OREB",
        "CAST(SUM(defensive_rebounds) AS SIGNED) AS DREB",
        "CAST(SUM(offensive_rebounds) + SUM(defensive_rebounds) AS SIGNED) AS REB",
        "CAST(SUM(assists) AS SIGNED) AS AST",
        "CAST(SUM(steals) AS SIGNED) AS STL",
        "CAST(SUM(blocks) AS SIGNED) AS BLK",
        "CAST(SUM(turnovers) AS SIGNED) AS 'TO'",
        "CAST(SUM(fouls) AS SIGNED) as PF"
    ]
}

select_args = {
    'basketball': basketball_select_args
}