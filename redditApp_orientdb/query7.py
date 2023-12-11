import requests
import base64
import json
import networkx as nx
import time


from bs4 import BeautifulSoup

def query7(X,db, benchmark = False):
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





    table = 'title_hyperlink'
    if db == 'new_db':
        table = 'body_hyperlink'
    query7 = f"SELECT DISTINCT subreddit_name  FROM (SELECT expand(out('{table}')) FROM Subreddit WHERE subreddit_name = '{X}') WHERE out('{table}').subreddit_name CONTAINS '{X}'"
    
    queryurl = f'http://localhost:2480/query/{db}/sql/{query7}'
    response = requests.get(queryurl, headers=headers)





    # Parse HTML content
    #soup = BeautifulSoup(response.content, 'html.parser')

    #print(soup.prettify())

    #create a graph visualization of the json response


    # Parse JSON response
    response_json = json.loads(response.text)


    names = []
    # Add nodes
    for node in response_json['result']:

       out_name = node['subreddit_name']

       if(benchmark == False):
        
            names.append(out_name)
    

    #disconnect
    disconnecturl= 'http://localhost:2480/disconnect'
    response = requests.get(disconnecturl, headers=headers)

    if(benchmark):
        end = time.time()
        #print(f"Query 7 - Database {db} took {end - start} seconds")
        return end - start
    return names