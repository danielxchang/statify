import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Utility Functions
def connect_to_db():
    mydb = mysql.connector.connect(
    host=os.environ.get('MYSQL_HOST'),
    user=os.environ.get('MYSQL_USER'),
    password=os.environ.get('MYSQL_PASSWORD'),
    database=os.environ.get('MYSQL_DB_DEV')
    )
    return mydb

def print_cursor(cursor):
    for x in cursor:
        print(x, type(x))

# Database Functions
def create_database(cursor, database_name):
    cursor.execute(f"CREATE DATABASE {database_name}")

def show_databases(cursor):
    cursor.execute("SHOW DATABASES")
    print_cursor(cursor)

def drop_database(cursor, database_name):
    cursor.execute(f"DROP DATABASE {database_name}")

'''
ALTER DATABASE
'''

# Table Functions
def use_table(cursor, table_name):
    cursor.execute(f"USE {table_name}")

def show_tables(cursor):
    cursor.execute("SHOW TABLES")
    print_cursor(cursor)

def create_table(cursor, table_name, columns_config):
    columns = [f"{name} {columns_config[name]}" for name in columns_config]
    query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
    cursor.execute(query)

def drop_table(cursor, table_name):
    cursor.execute(f"DROP TABLE {table_name}")

'''
ALTER TABLE
'''

# Data Query Functions
def select(cursor, table_name, columns = ['*'], options = None): 
    query = f'''
        SELECT {", ".join(columns)} 
        FROM {table_name}
    '''
    cursor.execute(query)

def insert_into():
    pass

def update():
    pass

def delete():
    pass


connected_db = connect_to_db()
mycursor = connected_db.cursor()

table_name = "customers"
columns_config = {
    "id": "INT AUTO_INCREMENT PRIMARY KEY",
    "name": "VARCHAR(255)",
    "address": "VARCHAR(255)"
}
select(mycursor, 'customers')
print_cursor(mycursor)

