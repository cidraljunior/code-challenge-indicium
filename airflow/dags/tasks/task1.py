import psycopg2
import pandas as pd
import os
import sys

date = sys.argv[1][:10]

#PostgreSQL Connection

host = "postgres-container-indicium"
database = "northwind"
user = "northwind_user"
password = "thewindisblowing"

db_conn = psycopg2.connect(host=host,database = database, user = user, password = password)
db_cursor = db_conn.cursor()

def get_table_names(db_cursor):

    table_names = []

    db_cursor.execute("""SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'""")

    for name in db_cursor.fetchall():
        table_names.append(name[0])

    return table_names

def csv_export(db_cursor,table_name,date):

    select = """SELECT * FROM {0}""".format(table_name)

    SQL_for_file_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(select)

    path_file = "/data/postgres/{0}/{1}/data.csv".format(table_name,date)

    os.makedirs(os.path.dirname(path_file), exist_ok = True)

    with open(path_file, 'w') as f_output:
        db_cursor.copy_expert(SQL_for_file_output, f_output)

for table_name in get_table_names(db_cursor):
    csv_export(db_cursor,table_name,date)
