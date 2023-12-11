import psycopg2
from psycopg2 import sql
import os
import shutil
import pandas as pd
import numpy as np
from datetime import datetime
import csv
import re
from tqdm import tqdm
import argparse

# Function to capture the iteration_number
def iteration_number(root_path):
    run_file= os.path.join(root_path, "run.txt")
    with open(run_file, "r") as f:
        line= f.readline()
        it_num= int(line[0])
    return it_num

# Function to update the iteration number
def update_it_num(root_path, current_it_num):
    run_file= os.path.join(root_path, "run.txt")
    with open(run_file, "w") as f:
        updated_it_num= str(current_it_num+1)
        f.write(f"{updated_it_num}") 

# Function to execute SQL file
def execute_sql_file(connection, file_path):
    with open(file_path, 'r') as file:
        sql_script = file.read()
        with connection.cursor() as cursor:
            cursor.execute(sql_script)
        connection.commit()

def copy_sql_file(connection, file_path):
    with open(file_path, 'r') as file:
        sql_script = file.read().split(";")
        sql_commands = [command.strip() for command in sql_script if command.strip()]
        with connection.cursor() as cursor:
            for command in sql_commands:
                cursor.execute(command)
        connection.commit()

# defining the parser 
parser = argparse.ArgumentParser()

# flags for obtaining and cleaning the data files
parser.add_argument("-rp", "--root_path", help="enter the root directory path")
# parser.add_argument("-qp", "--query_path", help="enter the path of all data files")
# parser.add_argument("-i", "--iteration_num", help="enter the iteration num")
# parser.add_argument("-sp", "--sub_param_path", help= "enter the path of substitution parameters")
parser.add_argument("-sf", "--scale_factor", help="enter the path of all data files")

args = parser.parse_args()

# defining the parameters
root_path= args.root_path
# query_path= args.query_path
scale_factor= args.scale_factor
# sub_params= args.sub_param_path

# setting the iteration number for the test
current_it= iteration_number(root_path= root_path)

# print start
print("----------------------------------------")
print(f"LOAD TEST: ITERATION {current_it}")
print("----------------------------------------") 

# Connection parameters
db_params = {
    'host': 'localhost',      
    'port': '5432',      
    'user': 'postgres',     
    'password': '1*@#Saymyname', 
}

# Database name
db_name = f'ldbcsnb_sf{scale_factor}'

# SQL file paths
schema_sql_file = '/mnt/d/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/ddl/schema.sql' 
data_sql_file = f'/mnt/d/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/ddl/load_sf{scale_factor}.sql'
schema_constraints_file="/mnt/d/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/ddl/schema_constraints.sql"
schema_foreign_keys_file= '/mnt/d/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/ldbc_snb_interactive_v1_impls/postgres/ddl/schema_foreign_keys.sql'

try:
    # Connect to the default PostgreSQL database (e.g., 'postgres')
    default_conn = psycopg2.connect(**db_params)
    default_conn.autocommit = True

    start_time= datetime.now()
    # Create a new database
    print(f"creating the new database {db_name}")
    with default_conn.cursor() as default_cursor:
        default_cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    print(f"database {db_name} created successfully")

    # Connect to the new database
    print(f"connecting to the newly created database {db_name}")
    conn_params = db_params.copy()
    conn_params['database'] = db_name
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True
    print(f"successfully connected to database {db_name}")

    # Execute schema SQL file
    print("Loading initial data set")
    execute_sql_file(conn, schema_sql_file)
    print("Schema loaded successfully.")
    
    # Execute data SQL file
    copy_sql_file(conn, data_sql_file)
    print("Data loaded successfully.")

    # loading the indexes and constraints 
    print("Adding indexes and constraints")
    execute_sql_file(conn, schema_constraints_file)
    print("Schema constraints loaded successfully.")
    
    # Execute data SQL file
    execute_sql_file(conn, schema_foreign_keys_file)
    print("Schema foreign keys loaded successfully.")

    # calculate  time
    print("load test stats being saved to a text file...")
    end_time= datetime.now()
    exec_time= (end_time - start_time).total_seconds()
    with open(os.path.join(root_path, f"load_test_stats_sf{scale_factor}.txt"), 'w') as f:
        f.write(f"Time taken for loading the data= {exec_time} seconds")
    print("load test stats saved to a text file")

except psycopg2.Error as e:
    print(f"Error: {e}")
finally:
    # Close connections
    if 'default_conn' in locals():
        default_conn.close()
    if 'conn' in locals():
        conn.close()