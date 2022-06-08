from database import *
from pprint import pprint

db_name = 'statify'
table_names = [
    'sports', 
    'users',
    'basketball_gamelogs',
    'leagues',
    'teams',
    'games',
    'players',
    'performances'
]
columns_configs = {
    'sports': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "sport_name": "VARCHAR(100) NOT NULL"
    },
    'users': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "first_name": "VARCHAR(100) NOT NULL",
        "middle_name": "VARCHAR(100)",
        "last_name": "VARCHAR(100) NOT NULL",
        "email": "VARCHAR(100)",
        "password": "VARCHAR(100)"
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
        "assists": "INT DEFAULT 0",
        "steals": "INT DEFAULT 0",
        "blocks": "INT DEFAULT 0",
        "turnovers": "INT DEFAULT 0",
        "fouls": "INT DEFAULT 0",
        "net_positive": 'BOOLEAN DEFAULT TRUE',
        "plus_minus": "INT DEFAULT 0",
        "points": "INT DEFAULT 0",
    },
    'leagues': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "league_name": "VARCHAR(100) NOT NULL",
        "city": "VARCHAR(100)",
        "state": "VARCHAR(100)",
        "country": "VARCHAR(100)",
        "sport_id": "INT NOT NULL",
        "FOREIGN KEY (sport_id)": "REFERENCES sports(id) ON DELETE CASCADE"
    },
    'teams': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "team_name": "VARCHAR(100) NOT NULL",
        "league_id": "INT",
        "sport_id": "INT NOT NULL",
        "FOREIGN KEY (league_id)": "REFERENCES leagues(id) ON DELETE CASCADE",
        "FOREIGN KEY (sport_id)": "REFERENCES sports(id) ON DELETE CASCADE"
    },
    'games': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "league_id": "INT NOT NULL",
        "team1_id": "INT NOT NULL",
        "team2_id": "INT NOT NULL",
        "team1_score": "INT DEFAULT 0",
        "team2_score": "INT DEFAULT 0",
        "FOREIGN KEY (league_id)": "REFERENCES leagues(id) ON DELETE CASCADE",
        "FOREIGN KEY (team1_id)": "REFERENCES teams(id) ON DELETE CASCADE",
        "FOREIGN KEY (team2_id)": "REFERENCES teams(id) ON DELETE CASCADE"
    },
    'players': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "user_id": "INT NOT NULL",
        "team_id": "INT NOT NULL",
        "position": "VARCHAR(100) NOT NULL",
        "FOREIGN KEY (user_id)": "REFERENCES users(id) ON DELETE CASCADE",
        "FOREIGN KEY (team_id)": "REFERENCES teams(id) ON DELETE CASCADE"
    },
    'performances': {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "game_id": "INT NOT NULL",
        "player_id": "INT NOT NULL",
        "gamelog_id": "INT NOT NULL",
        "FOREIGN KEY (game_id)": "REFERENCES games(id) ON DELETE CASCADE",
        "FOREIGN KEY (player_id)": "REFERENCES players(id) ON DELETE CASCADE",
        "FOREIGN KEY (gamelog_id)": "REFERENCES basketball_gamelogs(id) ON DELETE CASCADE"
    }
}

# Step 0 - Start from Scratch by Dropping Database
drop_database(db_name)

# Step 1 - Create and Select Database
create_database(db_name)
use_database(db_name)

# Step 2 - Create Tables 
for table_name in table_names:
    pprint(f'CREATING TABLE: {table_name}')
    create_table(table_name, columns_configs[table_name])

# Step 3 - Check for all table names
show_tables()

# Step 4 - Insert 'basketball' as first sport
insert_into_query('sports', ['sport_name'], [['"basketball"']])