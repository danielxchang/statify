'''
NOTE: WRAP ANY TEXT THAT WOULD ORDINARILY BE IN QUOTES IN A MYSQL QUERY IN NESTED QUOTES
'''

# TEST ARGUMENTS
database_name = 'statify_dev'
table_name = "players"
columns_config = {
    "id": "INT AUTO_INCREMENT PRIMARY KEY",
    "first_name": "VARCHAR(100)",
    "last_name": "VARCHAR(100)",
    "jersey_number": "INT",
    "team": "VARCHAR(100)",
    "position": "VARCHAR(100)"
}
select_arguments = {
    # 'SELECT': ['id', 'first_name', 'last_name', 'team', 'position'],
    'SELECT': ['id', 'CONCAT(first_name, " ", last_name) AS "full_name"', 'team', 'position'],
    # 'SELECT': ['team', 'COUNT(id) AS player_count'],
    "FROM": 'players',
    # "WHERE": 'jersey_number = 23',
    # "GROUP BY": ['team'],
    # "HAVING": "COUNT(id) >= 5",
    # "ORDER BY": ["player_count", "team"],
    # "LIMIT": {
    #     "count": 5,
    #     "offset": 0
    # },
}
insert_columns = ['first_name', 'last_name', 'jersey_number', 'team', 'position']
insert_values_list = [
    ["'Steph'", "'Curry'", "30", "'Golden State Warriors'", "'PG'"],
    ["'Draymond'", "'Green'", "23", "'Golden State Warriors'", "'SG'"],
    ["'Jordan'", "'Poole'", "3", "'Golden State Warriors'", "'PG'"],
    ["'Andrew'", "'Wiggins'", "22", "'Golden State Warriors'", "'SF'"],
    ["'Kevon'", "'Looney'", "5", "'Golden State Warriors'", "'C'"],
    ["'Luka'", "'Doncic'", "77", "'Dallas Mavericks'", "'PG'"],
    ["'Jalen'", "'Brunson'", "13", "'Dallas Mavericks'", "'PG'"],
    ["'Reggie'", "'Bullock'", "25", "'Dallas Mavericks'", "'SG'"],
    ["'Lebron'", "'James'", "6", "'Los Angeles Lakers'", "'SF'"],
    ["'Anthony'", "'Davis'", "3", "'Los Angeles Lakers'", "'PF'"],
    ["'Lavar'", "'Ball'", "1", "'Los Angeles Lakers'", "'PF'"]
]

update_set_assignments = ['position = "PF"']
update_where_condition = 'first_name = "Draymond"' 
delete_where_condition = 'first_name = "Lavar" AND last_name = "Ball"'


# TEST SEQUENCES
test_db_sequence = [
    'show db', 
    'create db', 
    'show db', 
    'use db', 
    'SELECT database()', 
    'drop db',
    'show db',
    'create db' 
]

test_table_sequence = [
    'use db',
    'show tables',
    'create table',
    'show tables',
    'drop table',
    'show tables',
    'create table'
]

test_data_query_sequence = [
    'use db',
    # TEST FOR EMPTY TABLE
    'select',
    'print query',
    # TEST INSERT INTO QUERY (Should see 11 records)
    'insert into',
    'select',
    'print query',
    # TEST UPDATE QUERY (Draymond Green's position should update to 'PF')
    'update',
    'select',
    'print query',
    # TEST DELETE QUERY (Lavar Ball should be deleted)
    'delete',
    'select',
    'print query'
]