-- Get Table Descriptions
DESC sports;
DESC leagues;
DESC positions;
DESC users;
DESC players;
DESC player_positions;
DESC teams;
DESC games;
DESC performances;
DESC basketball_gamelogs;

-- Select Statement for All Tables
SELECT * FROM sports;
SELECT * FROM leagues;
SELECT * FROM positions;
SELECT * FROM users;
SELECT * FROM players;
SELECT * FROM player_positions;
SELECT * FROM teams;
SELECT * FROM games;
SELECT * FROM performances;
SELECT * FROM basketball_gamelogs;


-- Checking that players have the right positions
/*
SELECT player_id, first_name, last_name, position 
FROM positions 
JOIN player_positions ON positions.id = player_positions.position_id
JOIN players ON players.id = player_positions.player_id 
JOIN users ON players.user_id = users.id
ORDER BY player_id;
*/
