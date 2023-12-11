
import requests
import base64
import json
import networkx as nx
import time
def query1(X,db, benchmark = False):
    

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
    
    
    query1 = f"""SELECT DISTINCT subreddit_name from (select expand(out('{table}'))from Subreddit where out('{table}').subreddit_name CONTAINS '{X}') 
                 where subreddit_name <> '{X}'"""


    queryurl = f'http://localhost:2480/query/{db}/sql/{query1}'
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
        name = node['subreddit_name']
        #remove the # from the rid
        names.append(name)
        


        if(benchmark == False):
            G.add_node(name)
    

        

    disconnecturl= 'http://localhost:2480/disconnect'
    response = requests.get(disconnecturl, headers=headers)
    if(benchmark):
        end = time.time()
       # print(f"Query 1 - Database {db} took {end - start} seconds")
        return (end-start)
    else:
        
        return (G,names) 

