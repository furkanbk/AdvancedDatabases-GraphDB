#create a http post to a certain text field

import requests
import base64
import json
import networkx as nx
import time


from bs4 import BeautifulSoup

def query3(db,benchmark = False):
    if(benchmark):
        start = time.time()
    connecturl = f'http://localhost:2480/connect/{db}'
    #Authorization HTTP header

    username = 'root'
    password = 'root'

    # Encode credentials in Base64
    credentials = f"{username}:{password}"
    credentials_encoded = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    # Create Authorization header
    headers = {'Authorization': f'Basic {credentials_encoded}'}
    response = requests.get(connecturl, headers=headers)



    #in fact query 3
    table = 'title_hyperlink'
    if db == 'new_db':
        table = 'body_hyperlink'
    query3 = f'SELECT in, count(*) as amount FROM (SELECT FROM {table} WHERE is_negative = false) GROUP BY in ORDER BY amount desc LIMIT 1'
    queryurl = f'http://localhost:2480/query/{db}/sql/{query3}'
    response = requests.get(queryurl, headers=headers)





    # Parse HTML content
    # soup = BeautifulSoup(response.content, 'html.parser')

    #print(soup.prettify())

    #create a graph visualization of the json response

    # Parse JSON response
    response_json = json.loads(response.text)

    # Create a directed graph
    G = nx.DiGraph()
    
    top_reddit = ''
    # Add nodes
    for node in response_json['result']:

    
        in_rid = node['in']
        #remove the # from the rid
        in_rid = in_rid[1:]
        in_name = ''
        query_for_name_in = f"SELECT * FROM subreddit WHERE @rid = '{in_rid}'"
        queryurl = f'http://localhost:2480/query/{db}/sql/{query_for_name_in}'
        response = requests.get(queryurl, headers=headers)
        #save the response as a json
        response_json_names = json.loads(response.text)

        for name in response_json_names['result']:
            in_name = name['subreddit_name']

        if(benchmark == False):
         
            G.add_node(in_name)
            top_reddit = in_name

    
    

    #disconnect
    disconnecturl= 'http://localhost:2480/disconnect'
    response = requests.get(disconnecturl, headers=headers)

    if benchmark:
        end = time.time()
        #print(f"Query 3 - Database {db} took {end - start} seconds")
        return end-start
    return (G, None, top_reddit) 