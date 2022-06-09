db_name = 'statify'
constraint_keywords = ['FOREIGN KEY', 'PRIMARY KEY', 'UNIQUE']

'''
To extend MySQL DB to new sports, just need to create a gamelogs
table for the new sport by defining its configuration and adding 
it to parent_tables_configs dictionary as key, value pair
'''
parent_tables_configs = {
    'sports': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "sport_name": "VARCHAR(100) UNIQUE NOT NULL"
    },
    'users': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "first_name": "VARCHAR(100) NOT NULL",
        "middle_name": "VARCHAR(100)",
        "last_name": "VARCHAR(100) NOT NULL",
        "email": "VARCHAR(100) UNIQUE NOT NULL",
        "password": "VARCHAR(100)",
        "created_at": "TIMESTAMP DEFAULT NOW()"
    },
    'basketball_gamelogs': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "minutes": "INT DEFAULT 0",
        "two_point_makes": "INT DEFAULT 0",
        "two_point_attempts": "INT DEFAULT 0",
        "three_point_makes": "INT DEFAULT 0",
        "three_point_attempts": "INT DEFAULT 0",
        "free_throw_makes": "INT DEFAULT 0",
        "free_throw_attempts": "INT DEFAULT 0",
        "offensive_rebounds": "INT DEFAULT 0",
        "defensive_rebounds": "INT DEFAULT 0",
        "assists": "INT DEFAULT 0",
        "steals": "INT DEFAULT 0",
        "blocks": "INT DEFAULT 0",
        "turnovers": "INT DEFAULT 0",
        "fouls": "INT DEFAULT 0",
        "net_positive": 'BOOLEAN DEFAULT TRUE',
        "plus_minus": "INT DEFAULT 0",
        "points": "INT DEFAULT 0",
    }
}

child_tables_configs = {
    'leagues': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "league_name": "VARCHAR(100) NOT NULL",
        "city": "VARCHAR(100)",
        "state": "VARCHAR(100)",
        "country": "VARCHAR(100)",
        "sport_id": "INT NOT NULL",
        "FOREIGN KEY": "(sport_id) REFERENCES sports(id) ON DELETE CASCADE"
    },
    'teams': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "team_name": "VARCHAR(100) NOT NULL",
        "league_id": "INT",
        "sport_id": "INT NOT NULL",
        "FOREIGN KEY": "(league_id) REFERENCES leagues(id) ON DELETE CASCADE",
        "FOREIGN KEY": "(sport_id) REFERENCES sports(id) ON DELETE CASCADE"
    },
    'games': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "date_played": "TIMESTAMP DEFAULT NOW()",
        "team1_id": "INT NOT NULL",
        "team2_id": "INT NOT NULL",
        "team1_score": "INT DEFAULT 0",
        "team2_score": "INT DEFAULT 0",
        "FOREIGN KEY": "(team1_id) REFERENCES teams(id) ON DELETE CASCADE",
        "FOREIGN KEY": "(team2_id) REFERENCES teams(id) ON DELETE CASCADE"
    },
    'players': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "user_id": "INT NOT NULL",
        "team_id": "INT NOT NULL",
        "FOREIGN KEY": "(user_id) REFERENCES users(id) ON DELETE CASCADE",
        "FOREIGN KEY": "(team_id) REFERENCES teams(id) ON DELETE CASCADE",
        "UNIQUE": "(user_id, team_id)"
    },
    'positions': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "position": "VARCHAR(100) NOT NULL",
        "sport_id": "INT NOT NULL",
        "FOREIGN KEY": "(sport_id) REFERENCES sports(id) ON DELETE CASCADE",
        "UNIQUE": "(position, sport_id)"
    },
    'player_positions': {
        "player_id": "INT NOT NULL",
        "position_id": "INT NOT NULL",
        "FOREIGN KEY": "(player_id) REFERENCES players(id) ON DELETE CASCADE",
        "FOREIGN KEY": "(position_id) REFERENCES positions(id) ON DELETE CASCADE",
        "PRIMARY KEY": "(player_id, position_id)"
    },
    'performances': {
        "game_id": "INT NOT NULL",
        "player_id": "INT NOT NULL",
        "gamelog_id": "INT NOT NULL",
        "FOREIGN KEY": "(game_id) REFERENCES games(id) ON DELETE CASCADE",
        "FOREIGN KEY": "(player_id) REFERENCES players(id) ON DELETE CASCADE",
        "FOREIGN KEY": "(gamelog_id) REFERENCES basketball_gamelogs(id) ON DELETE CASCADE",
        "PRIMARY KEY": "(game_id, player_id)"
    }
}

table_configs_map = {**parent_tables_configs, **child_tables_configs}