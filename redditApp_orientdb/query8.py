

import requests
import base64
import json
import networkx as nx
import time


from bs4 import BeautifulSoup

def query8(X,db, benchmark = False):
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
    

    
    query8_1 = f"select DISTINCT subreddit_name from (select expand(out('title_hyperlink')) from Subreddit WHERE subreddit_name = '{X}')"
    query8_1_1 = f"""
    
    SELECT other.subreddit_name as name, Count(*) as neg
    FROM(
    MATCH
        {{class: Subreddit, as: sbrdt, where: (subreddit_name = '{X}')}}.(outE('title_hyperlink'){{where: (is_negative = 1)}}.bothV()){{as:other}}
    Return
        other
    )
    group by other
     """
    
    queryurl = f'http://localhost:2480/query/{db}/sql/{query8_1_1}'
    response = requests.get(queryurl, headers=headers)



    response_json = json.loads(response.text)
    #print(response_json)

    negativities = {}

    for node in response_json['result']:
        negativities[node['name']] = node['neg']
     
    


    query8_1_2 = f"""
    SELECT other.subreddit_name as name, Count(*) as pos
    FROM(
    MATCH
        {{class: Subreddit, as: sbrdt, where: (subreddit_name = '{X}')}}.(outE('title_hyperlink'){{where: (is_negative = 0)}}.bothV()){{as:other}}
    Return
        other
    )
    group by other
    """

    queryurl = f'http://localhost:2480/query/{db}/sql/{query8_1_2}'
    response = requests.get(queryurl, headers=headers)


    response_json = json.loads(response.text)

    #print(response_json)

    positivities = {}

    for node in response_json['result']:
        positivities[node['name']] = node['pos']
    
    #print(positivities)
    #print(negativities)

    if(benchmark == False):

        #collect all keys from positivities and negativities into a set
        keys = set(positivities.keys()).union(negativities.keys())

        #for each key, if it exists in positivities and negativities, print the key and the values
        #else, print the key and 0
        for key in keys:
            if key in positivities and key in negativities:
                print (f"key {key} has positive: {positivities[key]} and negative: {negativities[key]}")
            elif key in positivities:
                print (f"key {key} has positive: {positivities[key]} and negative: 0")
            else:
                print (f"key {key} has positive: 0 and negative: {negativities[key]}")


        #if positivities has more keys than negativities, then add 0 to negativities for the missing keys


   
    
    # names = []
    # # Add nodes
    # for node in response_json['result']:

    #     out_name = node['subreddit_name']

    #     names.append(out_name)
    


    # negativities = []
    # for name in names:

    #     query8_2 = f"SELECT count(*) as neg_count FROM (select from title_hyperlink where out.subreddit_name = '{name}') where is_negative = true"
    #     query8_3 = f"SELECT count(*) as pos_count FROM (select from title_hyperlink where out.subreddit_name = '{name}') where is_negative = false"

    #     queryurl = f'http://localhost:2480/query/{db}/sql/{query8_2}'

    #     response = requests.get(queryurl, headers=headers)
    #     response_json = json.loads(response.text)

    #     neg_count = response_json['result'][0]['neg_count']

    #     queryurl = f'http://localhost:2480/query/{db}/sql/{query8_3}'
    #     response = requests.get(queryurl, headers=headers)
    #     response_json = json.loads(response.text)

    #     pos_count = response_json['result'][0]['pos_count']

    
    #     if(neg_count > pos_count):
    #         negativities.append(True)
    #     else:
    #         negativities.append(False)
        


    
    
    #disconnect
    disconnecturl= 'http://localhost:2480/disconnect'
    response = requests.get(disconnecturl, headers=headers)

    if(benchmark):
        end = time.time()
        #print(f"Query 8 - Database {db} took {end - start} seconds")
        return end - start
    return 