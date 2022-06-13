from database.database import *
from database.setup_db import get_db_map

class DataClerk:
    def __init__(self, sport):
        self.init_db_map(sport)

    def init_db_map(self, sport):
        self.db_name, self.db_columns = get_db_map(sport)

    def query_database(self, query_type, query_args):
        if query_type == 'INSERT_INTO':
            return self.insert(query_args)
        if query_type == 'SELECT':
            return self.select(query_args)
        if query_type == 'UPDATE':
            return self.update(query_args)

    def insert(self, query_args):
        table_name = query_args['table_name']
        columns = query_args['columns']
        values_list = query_args['values_list']
        insert_into_query(table_name, columns, values_list)
        return get_last_insert_id()

    def select(self, query_args):
        select_query(query_args)
        return get_last_query()

    def update(self, query_args):
        table_name = query_args['table_name']
        set_assignments = query_args['set_assignments']
        where_condition = query_args['where_condition']
        update_query(table_name, set_assignments, where_condition)

    def does_record_exist(self, select_query_args):
        match_records = self.query_database('SELECT', select_query_args)['records']
        return match_records[0][0] if len(match_records) else False

    def print_insert_count(self, count, table_name):
        print(f'TABLE {table_name}: {count} new record(s) added')

    def format_input(self, input):
        return f'"{input}"' if type(input) == str else str(input)

    def format_input_list(self, input_list, join_sep = ', '):
        return join_sep.join([self.format_input(input_item) for input_item in input_list])

    def insert_into_db(self, table_name, insert_entry = {}):
        columns = [
            col for col in self.db_columns[table_name] 
            if col in insert_entry and insert_entry[col]
        ]
        values = [[self.format_input(insert_entry[col]) for col in columns]]
        insert_args = {
            'table_name': table_name, 
            'columns': columns,
            'values_list': values
        }
        return self.query_database('INSERT_INTO', insert_args)