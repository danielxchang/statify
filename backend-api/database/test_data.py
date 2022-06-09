'''
NOTE: WRAP ANY TEXT THAT WOULD ORDINARILY BE IN QUOTES IN A MYSQL QUERY IN NESTED QUOTES
'''
# Sets variables to corresponding table data
def set_data_input_variables(table):    
    var_group = variable_map[table]
    table_name = var_group['table_name']
    columns_config = var_group['columns_config']
    select_arguments = var_group['select_arguments']
    insert_columns = var_group['insert_columns']
    insert_values_list = var_group['insert_values_list']
    test_data_query_sequence = var_group["test_data_query_sequence"]
    update_set_assignments = var_group['update_set_assignments'] if table == 'child' else None
    update_where_condition = var_group['update_where_condition'] if table == 'child' else None
    delete_where_condition = var_group['delete_where_condition'] if table == 'child' else None
    return table_name, columns_config, select_arguments, insert_columns, insert_values_list, update_set_assignments, update_where_condition, delete_where_condition, test_data_query_sequence

database_name = 'statify_dev'

# Table Name Variables
parent_table_name = "teams"
child_table_name = "players"

# Columns Configuration Variables
parent_columns_config = {
    "id": "INT AUTO_INCREMENT PRIMARY KEY",
    "team": "VARCHAR(100)"
}
child_columns_config = {
    "id": "INT AUTO_INCREMENT PRIMARY KEY",
    "first_name": "VARCHAR(100)",
    "last_name": "VARCHAR(100)",
    "jersey_number": "INT",
    "team_id": "INT",
    "position": "VARCHAR(100)",
    "FOREIGN KEY": "(team_id) REFERENCES teams(id) ON DELETE CASCADE"
}

# Select variables
parent_select_arguments = {
    'SELECT': ['*'],
    "FROM": 'teams'
}
child_select_arguments = {
    # 'SELECT': ['id', 'first_name', 'last_name', 'team', 'position'],
    'SELECT': ['CONCAT(first_name, " ", last_name) AS "full_name"', 'team', 'position'],
    # 'SELECT': ['team', 'COUNT(id) AS player_count'],
    "FROM": 'players',
    "JOIN": [
        ["INNER", 'teams', 'teams.id = players.team_id']
    ]
    # "WHERE": 'jersey_number = 23',
    # "GROUP BY": ['team'],
    # "HAVING": "COUNT(id) >= 5",
    # "ORDER BY": ["player_count", "team"],
    # "LIMIT": {
    #     "count": 5,
    #     "offset": 0
    # },
}

# Insert Data Variables
parent_insert_columns = ['team']
parent_insert_values_list = [
    ["'Golden State Warriors'"],
    ["'Dallas Mavericks'"],
    ["'Los Angeles Lakers'"]
]
child_insert_columns = ['first_name', 'last_name', 'jersey_number', 'team_id', 'position']
child_insert_values_list = [
    ["'Steph'", "'Curry'", "30", "1", "'PG'"],
    ["'Draymond'", "'Green'", "23", "1", "'SG'"],
    ["'Jordan'", "'Poole'", "3", "1", "'PG'"],
    ["'Andrew'", "'Wiggins'", "22", "1", "'SF'"],
    ["'Kevon'", "'Looney'", "5", "1", "'C'"],
    ["'Luka'", "'Doncic'", "77", "2", "'PG'"],
    ["'Jalen'", "'Brunson'", "13", "2", "'PG'"],
    ["'Reggie'", "'Bullock'", "25", "2", "'SG'"],
    ["'Lebron'", "'James'", "6", "3", "'SF'"],
    ["'Anthony'", "'Davis'", "3", "3", "'PF'"],
    ["'Lavar'", "'Ball'", "1", "3", "'PF'"]
]

# Update and Delete variables
child_update_set_assignments = ['position = "PF"']
child_update_where_condition = 'first_name = "Draymond"' 
child_delete_where_condition = 'first_name = "Lavar" AND last_name = "Ball"'


# TEST SEQUENCES
test_db_sequence = [
    'drop db',
    'show db', 
    'create db', 
    'show db', 
    'use db', 
    'SELECT database()'
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

parent_test_data_query_sequence = [
    'use db',
    # TEST INSERT INTO QUERY (Should see 11 records)
    'insert into',
    'select',
    'print query'
]

child_test_data_query_sequence = [
    'use db',
    # TEST FOR EMPTY TABLE
    'select',
    'print query',
    # TEST INSERT INTO QUERY (Should see 11 records)
    'insert into',
    'SELECT * FROM players',
    # TEST SELECT QUERY (WITH JOIN CLAUSE)
    'select',
    'print query',
    # TEST UPDATE QUERY (Draymond Green's position should update to 'PF')
    'update',
    'select',
    'print query',
    # TEST DELETE QUERY with players table (Lavar Ball should be deleted)
    'delete',
    'select',
    'print query'
]

# Mapping of Variables to corresponding table
variable_map = {
    "parent": {
        'table_name': parent_table_name,
        'columns_config': parent_columns_config,
        'select_arguments': parent_select_arguments,
        'insert_columns': parent_insert_columns,
        'insert_values_list': parent_insert_values_list,
        "test_data_query_sequence": parent_test_data_query_sequence
    },
    "child": {
        'table_name': child_table_name,
        'columns_config': child_columns_config,
        'select_arguments': child_select_arguments,
        'insert_columns': child_insert_columns,
        'insert_values_list': child_insert_values_list,
        'update_set_assignments': child_update_set_assignments,
        'update_where_condition': child_update_where_condition,
        'delete_where_condition': child_delete_where_condition,
        "test_data_query_sequence": child_test_data_query_sequence
    }
}