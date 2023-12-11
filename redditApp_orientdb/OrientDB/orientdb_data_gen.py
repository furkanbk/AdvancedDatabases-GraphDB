import pandas as pd
from datetime import datetime
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

def convert_ts_format(column, date_format):
    for ele in column:
        ele= datetime.strptime(ele, date_format)
    print(column)

def convert_bool(column):
    column = column.replace({0: False, 1: True})
    print(column.describe())

def vertex_creation():
    query=(f"CREATE CLASS Subreddit EXTENDS V;"
           f" CREATE PROPERTY Subreddit.subredditName STRING;")
    
    return query

# example edge creation code
# CREATE EDGE body_hyperlink
# FROM (Select from subreddit where subreddit_name= 'rddtgaming')
# TO (Select from subreddit where subreddit_name= 'bestof')
# CONTENT{ 'is_negative' : true,
#     'LIWC_anger' : 0.5,
#     'LIWC_dissent' : 0.3,
#     'LIWC_sad' : 0.2,
#     'LIWC_swear' : 0.1,
#     'postID' : '123456',
#     'timestamp' : '2012-12-14  17:59:40'}
def title_edge_creation():
    query= (f"CREATE CLASS title_hyperlink EXTENDS E;" 
    f" CREATE PROPERTY title_hyperlink.post_id STRING;" 
    f" CREATE PROPERTY title_hyperlink.timestamp DATETIME;" 
    f" CREATE PROPERTY title_hyperlink.is_negative BOOLEAN;"
    f" CREATE PROPERTY title_hyperlink.LIWC_swear DOUBLE;"
    f" CREATE PROPERTY title_hyperlink.LIWC_anger DOUBLE;"
    f" CREATE PROPERTY title_hyperlink.LIWC_sad DOUBLE;" 
    f" CREATE PROPERTY title_hyperlink.LIWC_dissent DOUBLE;")

    return query

def edge_insertion_title(dataframe):
    # edge insertion
    edge_creation = []
    hyperlink_type= 'title_hyperlink'
    for index, row in dataframe.iterrows():
        query = (
            f"CREATE EDGE {hyperlink_type}"
            f" FROM (SELECT FROM subreddit WHERE subreddit_name = '{row['SOURCE_SUBREDDIT']}')"
            f" TO (SELECT FROM subreddit WHERE subreddit_name = '{row['TARGET_SUBREDDIT']}')"
            f" CONTENT {{ 'is_negative' : {row['IS_NEGATIVE']}, "
            f" 'LIWC_anger' : {row['LIWC_Anger']}, "
            f" 'LIWC_dissent' : {row['LIWC_Dissent']}, "
            f" 'LIWC_sad' : {row['LIWC_Sad']}, "
            f" 'LIWC_swear' : {row['LIWC_Swear']}, "
            f" 'postID' : '{row['POST_ID']}', "
            f" 'timestamp' : '{row['TIMESTAMP']}' }};"
        )
        edge_creation.append(query)

    return edge_creation

# function to truncate csv file to generate different scale factor data
def truncate(df, value):
    return df[:value]

# extract unique vertices from data
def extract_unique_data(df):
    source_unique_values = set(df['SOURCE_SUBREDDIT'].unique())
    target_unique_values = set(df['TARGET_SUBREDDIT'].unique())
    unique_values= list(source_unique_values.union(target_unique_values))
    print(f"number of unique vertices= {len(unique_values)}\n")
    return unique_values

parser = argparse.ArgumentParser()
parser.add_argument("-rp", "--root_path", help="enter the root directory path")
parser.add_argument("-fp", "--file_path", help="enter the path of all csv data files")
parser.add_argument("-sf", "--scale_factor", help="enter the scale factor")

args = parser.parse_args()

# defining the parameters
root_path= args.root_path
file_path= args.file_path
scale_factor= args.scale_factor

# Read the CSV file
df_title = pd.read_csv(os.path.join(file_path, 'title.csv'))
df_body= pd.read_csv(os.path.join(file_path, 'body.csv'))

# creating different scale factors
df_title= truncate(df_title, int(scale_factor))
print(df_title.shape)

# Extract unique values from the SUBREDDIT column
# unique_values= extract_unique_data(df_title_5k)
unique_values= extract_unique_data(df_title)

# Define the format of the input date string
date_format = "%Y-%m-%d %H:%M:%S"

# Convert the date string to a datetime object
# convert_ts_format(df_title_5k['TIMESTAMP'], date_format)
convert_ts_format(df_title['TIMESTAMP'], date_format)

# convert boolean 1 to true and 0 to false
convert_bool(df_title['IS_NEGATIVE'])
# convert_bool(df_title_1k['IS_NEGATIVE'])

# Generate the SQL query
vertex_insert = "INSERT INTO subreddit(subreddit_name) VALUES " + ', '.join(f"('{value}')" for value in unique_values) 

# body_hyperlink_query_list= edge_insertion_body(df_body)
title_hyperlink_query_list= edge_insertion_title(df_title)

# Save the code to a text file
print("writing the file to load the database...")
with open(f'load_reddit_db_{scale_factor}.osql', 'w') as file:
    file.write("--Vertex Creation\n")
    file.write(vertex_creation())
    file.write("\n\n")
    file.write("--Title Edge Creation\n")
    file.write(title_edge_creation())
    file.write("\n\n")
    file.write("--Vertex insertion\n")
    file.write(vertex_insert + ";\n")
    file.write("\n")
    file.write("--Title Hyperlink Edge Insertion\n")
    file.write('\n'.join(title_hyperlink_query_list))