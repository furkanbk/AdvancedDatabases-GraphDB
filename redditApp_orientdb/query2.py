
import requests
import base64
import json
import networkx as nx
import time
def query2(X,db, benchmark = False):
    if(benchmark):
        #start the timer
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

    #print(f"Connection: {response.status_code}")

    table = 'title_hyperlink'
    if db == 'new_db':
        table = 'body_hyperlink'
    query2 = f"SELECT FROM( SELECT expand(outE('{table}')) FROM subreddit WHERE subreddit_name = '{X}') WHERE is_negative = true"

    queryurl = f'http://localhost:2480/query/{db}/sql/{query2}'
    response = requests.get(queryurl, headers=headers)


    # Parse HTML content

    #soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup.prettify())



    #create a graph visualization of the json response


    # Parse JSON response
    response_json = json.loads(response.text)

    # Create a directed graph
    G = nx.DiGraph()
    names = []
    # Add nodes
    for node in response_json['result']:

        #get the rid of the subreddit
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
        

        #get the rid of the subreddit
        out_rid = node['out']
        #remove the # from the rid
        out_rid = out_rid[1:]
        out_name = '' 
        query_for_name_out = f"SELECT * FROM subreddit WHERE @rid = '{out_rid}'"
        queryurl = f'http://localhost:2480/query/{db}/sql/{query_for_name_out}'
        response = requests.get(queryurl, headers=headers)
        #save the response as a json
        response_json_names = json.loads(response.text)

        for name in response_json_names['result']:
            out_name = name['subreddit_name']

        if(benchmark == False):
            G.add_node(in_name)
            G.add_node(out_name)
            G.add_edge(in_name, out_name)
            #add a label to the edge
            G.edges[in_name, out_name]['is_negative'] = node['is_negative']
            names.append(in_name)
            #G.edges[in_name, out_name]['LIWC_anger'] = node['LIWC_anger']

        # G.edges[edge['in'], edge['out']]['is_negative'] = edge['is_negative']
        # G.edges[edge['in'], edge['out']]['LIWC_anger'] = edge['LIWC_anger']

    disconnecturl= 'http://localhost:2480/disconnect'
    response = requests.get(disconnecturl, headers=headers)
    if(benchmark):
        end = time.time()
       # print(f"Query 2 - Database {db} took {end - start} seconds")
        return end - start
    else:
        edge_labels = {(u, v): f"is_negative = {G.edges[u, v]['is_negative']}" for u, v in G.edges}
        return (G, edge_labels, names) 

