import mysql.connector
from dotenv import load_dotenv
from pprint import pprint
import os

load_dotenv()

# All-Purpose Query Function
def execute_custom_query(query):
    return execute_query(query)

# Utility Functions
def connect_to_db():
    mydb = mysql.connector.connect(
    host=os.environ.get('MYSQL_HOST'),
    user=os.environ.get('MYSQL_USER'),
    password=os.environ.get('MYSQL_PASSWORD')
    )
    return mydb

def get_last_query():
    query_data = {
        "headings": cursor.column_names,
        "records": cursor.fetchall()
    }
    return query_data

def get_table_columns(table_name):
    execute_custom_query(f"SHOW columns FROM {table_name}")
    return [column[0] for column in cursor.fetchall()] 

def get_table_description(table_name):
    execute_custom_query(f'DESC {table_name}')
    return get_last_query()

def get_last_insert_id():
    execute_custom_query("SELECT LAST_INSERT_ID()")
    return get_last_query()['records'][0][0]

def commit_changes():
    connected_db.commit()

def close_db():
    connected_db.close()

def execute_query(query, commit_change = False):
    try:
        cursor.execute(query)
        if commit_change:
            commit_changes()
        return True, {"message": 'Success!', "query": query}
    except mysql.connector.Error as err:
        return False, {"message": err, "query": query}

def print_cursor():
    for x in cursor:
        print(x)

# Database Functions
def show_databases():
    result = execute_query("SHOW DATABASES")
    print_cursor()
    return result

def create_database(database_name):
    return execute_query(f"CREATE DATABASE {database_name}")

def use_database(database_name):
    return execute_query(f"USE {database_name}")

def drop_database(database_name):
    return execute_query(f"DROP DATABASE IF EXISTS {database_name}")

# Table Functions
def show_tables():
    result = execute_query("SHOW TABLES")
    print_cursor()
    return result

def create_table(table_name, columns_config):
    columns = [f"{name} {columns_config[name]}" for name in columns_config]
    query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
    return execute_query(query)

def drop_table(table_name):
    return execute_query(f"DROP TABLE {table_name}")

# Data Query Functions
def select_query(clause_arguments): 
    query_statements = []
    for clause in ["SELECT", "FROM", 'JOIN', "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT"]:
        if clause in clause_arguments:
            query_statements.append(select_handler(clause, clause_arguments[clause]))
    
    query = '\n'.join(query_statements)
    return execute_query(query)

def insert_into_query(table_name, columns, values_list):
    columns_string = ', '.join(columns)
    values_string = '), \n('.join([', '.join(values) for values in values_list])
    query = f"INSERT INTO {table_name} ({columns_string}) \nVALUES \n({values_string})"
    return execute_query(query, True)

def update_query(table_name, set_assignments, where_condition):
    assignments_string = ',\n'.join(set_assignments)
    query = f"UPDATE {table_name} \nSET \n{assignments_string} \nWHERE {where_condition}"
    return execute_query(query, True)

def delete_query(table_name, where_condition):
    query = f"DELETE FROM {table_name} \nWHERE {where_condition}"
    return execute_query(query, True)

def select_handler(clause, specifications):
    if clause == 'SELECT':
        return select(specifications)
    if clause == 'FROM':
        return from_clause(specifications)
    if clause == 'JOIN':
        return join(specifications)
    if clause == 'WHERE':
        return where(specifications)
    if clause == 'ORDER BY':
        return order_by(specifications)
    if clause == 'GROUP BY':
        return group_by(specifications)
    if clause == 'HAVING':
        return having(specifications)
    if clause == 'LIMIT':
        return limit(specifications)

def select(columns):
    return f"SELECT {', '.join(columns)}"

def from_clause(table_name):
    return f"FROM {table_name}"

def join(join_statements):
    joins = [f"{j_type} JOIN {table} ON {condition}" for j_type, table, condition in join_statements]
    return '\n'.join(joins)

def where(search_condition):
    return f"WHERE {search_condition} "

def order_by(expressions):
    return f"ORDER BY {', '.join(expressions)}"

def group_by(expressions):
    return f"GROUP BY {', '.join(expressions)}"

def having(group_condition):
    return f"HAVING {group_condition}"

def limit(arguments):
    return f"LIMIT {arguments['offset'] if 'offset' in arguments else 0}, {arguments['count']}" 

connected_db = connect_to_db()
cursor = connected_db.cursor()