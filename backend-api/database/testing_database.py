from database import *
from pprint import pprint
from testing_data import *

# Database Functions Tests
def test_show_db():
    return show_databases()

def test_use_db():
    return use_database(database_name)

def test_create_db():
    return create_database(database_name)

def test_drop_db():
    return drop_database(database_name)

# Table Functions Tests
def test_create_table():
    return create_table(table_name, columns_config)

def test_drop_table():
    return drop_table(table_name)

def test_show_tables():
    return show_tables()

# Data Query Function Tests
def test_select():
    return select_query(select_arguments)

def test_insert_into():
    return insert_into_query(table_name, insert_columns, insert_values_list)

def test_update():
    return update_query(table_name, update_set_assignments, update_where_condition)

def test_delete():
    return delete_query(table_name, delete_where_condition)

# Utility Helper Functions
def get_query_result():
    return True, get_last_query()

def get_columns():
    return True, get_table_columns(table_name)

# Testing Execution Functions
def run_tests(test_group, custom_sequence = None):
    if test_group == 'DB':
        test_sequence = test_db_sequence
    elif test_group == 'TABLE':
        test_sequence = test_table_sequence
    elif test_group == 'QUERY':
        test_sequence = test_data_query_sequence
    else:
        test_sequence = custom_sequence

    passed_tests = 0
    for i, test in enumerate(test_sequence):
        print(f"----------------------------------TEST {i + 1}----------------------------------")
        if not test_db_function(test):
            return 
        passed_tests += 1
    print(f"----------------------------------------------------------------------------")
    print(f"Passed {passed_tests} of {len(test_sequence)} tests!")

def test_db_function(test_type):
    passed, response = tests[test_type]() if test_type in tests else execute_custom_query(test_type)
    print(f"QUERY: {test_type}")
    pprint(response)
    if test_type not in tests:
        print_cursor()
    return passed

# Test keyword to test function map
tests = {
    'create db': test_create_db, 
    'drop db': test_drop_db, 
    'use db': test_use_db, 
    'show db': test_show_db,
    'create table': test_create_table, 
    'drop table': test_drop_table,
    'show tables': test_show_tables, 
    'select': test_select,
    'insert into': test_insert_into,
    'update': test_update,
    'delete': test_delete,
    'print query': get_query_result,
    'print columns': get_columns
}

'''
Helpful database management code for setting up / cleaning changes made during testing
run_tests('CUSTOM', ['create db', 'show db']) # SET UP TEST DATABASE
run_tests('CUSTOM', ['drop db']) # DROP TEST DATABASE
run_tests('CUSTOM', ['create table', 'show tables']) # CREATE TEST TABLE
run_tests('CUSTOM', ['drop table']) # DROP TEST TABLE

Uncomment and run any of the lines below to test function groups individually
Uncomment all and run to run all tests at once
'''

run_tests('DB')
run_tests('TABLE')
run_tests('QUERY')
run_tests('CUSTOM', ['drop db']) # RESET DB BY DROP TEST DB
close_db()