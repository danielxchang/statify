-- Get Table Descriptions
/*
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
*/

-- Select Statement for All Tables
/*
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
*/

-- Checking that players have the right positions
/*
SELECT player_id, first_name, last_name, position 
FROM positions 
JOIN player_positions ON positions.id = player_positions.position_id
JOIN players ON players.id = player_positions.player_id 
JOIN users ON players.user_id = users.id
ORDER BY player_id;
*/

-- Join gamelogs with player names
/*
SELECT 
    CONCAT(users.first_name, ' ', users.last_name) AS 'full_name', 
    basketball_gamelogs.*
FROM basketball_gamelogs
JOIN performances
    ON performances.gamelog_id = basketball_gamelogs.id
JOIN players
    ON players.id = performances.player_id
JOIN users
    ON users.id = players.user_id;
*/

-- Box Score Query: Individual Players
/*
SELECT 
    team_name AS team,
    CONCAT(users.first_name, ' ', users.last_name, ' ', position) AS player, 
    CAST(ROUND((minutes_played * 60 + seconds_played) / 60, 0) AS SIGNED) AS MIN,
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
JOIN teams
    ON players.team_id = teams.id
ORDER BY team_id;
*/

-- Box Score Query: Team
/*
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
*/

-- Get Game Data for existing game_id
/*
SELECT team_name, team_id, gamelog_id
FROM performances
JOIN players
    ON performances.player_id = players.id
JOIN teams
    ON teams.id = players.team_id
WHERE game_id = 1;
*/

-- Get all games with team names displayed
/*
SELECT
    games.id AS game_id,
    date_played,
    (SELECT team_name FROM teams WHERE teams.id = team1_id) AS team1_name,
    (SELECT team_name FROM teams WHERE teams.id = team2_id) AS team2_name,
    team1_score,
    team2_score
FROM games
GROUP BY game_id;
*/