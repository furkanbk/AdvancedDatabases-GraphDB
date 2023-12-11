import psycopg2 as pg
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

# Function to extract the query number
def extract_query_num(filename):
    res= re.split("[ _ | . ]", filename)
    num= int(res[1])
    return num

def get_number(filename):
    # Extract the number using a regular expression
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 0

# Function to read parameters from text file
def read_parameters(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    column_list= lines[0].split("|")
    column_list[-1]= column_list[-1][:-1]
    print(column_list)
    parameters_dict={}
    for i in column_list:
      parameters_dict[f'{i}']=[]

    for line in lines[1:]:  # Skip the header line
      line= line.rstrip('\n')
      value_list= line.split('|')
      for i, key in enumerate(column_list):
        parameters_dict[key].append(value_list[i])

    return parameters_dict

# Function to read SQL query from file
def read_sql_query(file_path):
    with open(file_path, 'r') as file:
        sql_query = file.read()
    return sql_query

# Function to execute PostgreSQL query
def execute_query(connection, sql_query):
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        result = cursor.fetchall()
    return result

def list_queries(query_list):
    count=1
    interactive_complex_queries_list= []
    rest_queries= []
    for filename in query_list:
        if(count<=14):
            interactive_complex_queries_list.append(filename)
        else:
            rest_queries.append(filename)
        count+=1
    interactive_complex_queries_list_sorted= sorted(interactive_complex_queries_list, key=get_number)
    interactive_complex_queries_list= interactive_complex_queries_list_sorted
    interactive_complex_queries_list.extend(rest_queries)
    final_query_list= interactive_complex_queries_list

    return final_query_list

# Function to execute SQL queries and log execution times
def execute_queries(root_path, sql_folder, scale_factor, it_num, params):
    conn = pg.connect(**db_params)
    cur = conn.cursor()
    wrong_query_list=[]
    sql_file_list=[]
    stats_list=[]

    param_file_list= os.listdir(params)
    param_file_list_sorted= sorted(param_file_list, key=get_number)
    param_file_list= param_file_list_sorted
    print(param_file_list)

    for filename in os.listdir(sql_folder):
        if filename.endswith(".sql"):
            sql_file_list.append(filename)
    
    # sorted_sql_file_list= sorted(sql_file_list, key=extract_query_num)
    # sql_file_list= sorted_sql_file_list
    final_query_list= list_queries(sql_file_list)
    print(final_query_list)

    with tqdm(total= len(sql_file_list)) as pbar:
        for file_num, filename in enumerate(final_query_list):
            query_file = os.path.join(sql_folder, filename)

            # read the sql file
            sql_query = read_sql_query(query_file)
            
            # Read substitution parameters
            sub_param_filepath= os.path.join(params, param_file_list[file_num])
            substitution_parameters = read_parameters(sub_param_filepath)
            print(substitution_parameters)
            key_list= list(substitution_parameters.keys())

            # Replace placeholders in the SQL query
            count=0
            start_time = datetime.now()
            for i in range(len(substitution_parameters[key_list[0]])):
                query_instance = sql_query  # Create a copy of the original query
                count+=1
                query_list=[]
                # Replace placeholders with values from the dictionary
                # count=0
                for key, values_list in substitution_parameters.items():
                    placeholder = f":{key}"
                    print(placeholder)
                    value = f"'{values_list[i]}'"
                    if(key=='personId' or key=='person1Id' or key=='person2Id'):
                        cleaned_string = value.strip("'")
                        value= f"{cleaned_string}"
                    if(key=='durationDays' or key=='month'):
                        cleaned_string = value.strip("'")
                        value= f"{cleaned_string}"
                    if(key=='maxDate' or key=='startDate' or key=='minDate'):
                        cleaned_string = value.strip("'")
                        value= f"TO_TIMESTAMP({cleaned_string} / 1000.0)"
                    print(value)
                    query_instance = query_instance.replace(placeholder, value)
                    query_list.append(query_instance)

                # printing the result
                print("----------------------")
                print(f"Query {count} result")
                print("----------------------")
                try:
                    cur.execute(query_instance)
                    result= cur.fetchall()
                    conn.commit()
                    print(result)
                except Exception as e:
                    conn.rollback()
                    wrong_query_list.append(filename)
                    print(f" '{filename}': Error executing query : {e}")
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            stats_list.append([filename, start_time, end_time, execution_time])
            pbar.set_postfix(file=filename, start=start_time, end=end_time, time=execution_time)
            pbar.update(1)
            print(f" '{filename}' executed successfully in {execution_time} seconds.")
            print(f"Total number of queries executed= {count}")
    
    # printing the list of queries that are wrong
    if len(wrong_query_list)!=0:
        print(wrong_query_list)
    else:
        print("No wrong query found during processing")
    
    # save the stats to a csv file 
    print("saving the pandas dataframe to a csv...")
    df= pd.DataFrame(stats_list, columns=["Query File", "Start Time", "End Time", "Execution Time"])
    df.to_csv(os.path.join(root_path, f'benchmark_stats_sf_{scale_factor}_it_{it_num}.csv'), index=False)
    print(f"query stats for scale factor {scale_factor} saved successfully")
    cur.close()
    conn.close()

parser = argparse.ArgumentParser()

# flags for obtaining and cleaning the data files
parser.add_argument("-rp", "--root_path", help="enter the root directory path")
parser.add_argument("-qp", "--query_path", help="enter the path of all data files")
parser.add_argument("-sp", "--sub_param_path", help= "enter the path of substitution parameters")
parser.add_argument("-sf", "--scale_factor", help="enter the scale factor")

args = parser.parse_args()

# defining the parameters
root_path= args.root_path
query_path= args.query_path
scale_factor= args.scale_factor
sub_params= args.sub_param_path

# setting the iteration number for the test
current_it= iteration_number(root_path= root_path)

# print start
print("----------------------------------------")
print(f"BENCHMARK: ITERATION {current_it}")
print("----------------------------------------") 

# Defining the connection parameters
db_params = {
    "host": "localhost",
    "database": f"ldbcsnb_sf{scale_factor}",
    "user": "postgres",
    "password": "1*@#Saymyname"
}

# Establish a connection to the PostgreSQL database
try:
    conn = pg.connect(**db_params)
    print("Connected to the database")
except Exception as e:
    print(f"Error: {e}")

# Create a cursor object to interact with the database
cur = conn.cursor()
# printing the version 
cur.execute("SELECT version();")
print("PostgreSQL version:")
print(cur.fetchone())

# executing the queries
st_time= datetime.now()
execute_queries(root_path= root_path, sql_folder= query_path, scale_factor= scale_factor, it_num= current_it, params= sub_params)
end_time= datetime.now()

# calculate the total execution time
exec_time = (end_time - st_time).total_seconds()
exec_time_minutes= exec_time/60

# logging the results into a text file
with open(os.path.join(root_path, f"benchmark_stats_sf{scale_factor}.txt"), "a") as f:
    f.write(f"Iteration {current_it}: Total time taken to execute queries with scale factor {scale_factor}= {exec_time} seconds\n")

# logging the execution times
print(f"total time taken: {exec_time_minutes} minutes")

# updatiun the iteration number
update_it_num(root_path, current_it)

# Close the cursor and the connection when you're done
cur.close()
conn.close()