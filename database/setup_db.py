from database.database import *
from pprint import pprint
from database.setup_db_data import db_name, table_configs_map, constraint_keywords
import re

def run_setup_queries():
    # Step 0 - Start from Scratch by Dropping Database
    drop_database(db_name)

    # Step 1 - Create and Select Database
    create_database(db_name)
    use_database(db_name)

    # Step 2 - Create Tables 
    for table_name in table_configs_map:
        pprint(f'CREATING TABLE: {table_name}')
        success, response = create_table(table_name, table_configs_map[table_name])
        if not success:
            print(response)
            break

    # Step 3 - Check for all table names
    show_tables()

    # Step 4 - Insert 'basketball' as first sport in sports table
    insert_into_query('sports', ['sport_name'], [['"basketball"']])

    # Step 5 - Insert basketball positions into positions table
    basketball_positions = ['PG', 'SG', 'SF', 'PF', 'C']
    for pos in basketball_positions:
        insert_into_query('positions', ['position', 'sport_id'], [[f'"{pos}"', '1']])

def get_db_map(sport):
    gamelog_table = f"{sport}_gamelogs"
    table_columns_map = { 
        table_name: [
            key for key in table_configs_map[table_name] if key not in constraint_keywords
        ] 
        for table_name in table_configs_map 
        if not re.search("_gamelogs$", table_name) or table_name == gamelog_table
    }

    return db_name, table_columns_map

def run_db_checks():
    show_tables()
    select_query({
        'SELECT': ['*'],
        'FROM': 'games'
    })
    last_result = get_last_query()
    pprint(last_result)