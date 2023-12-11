# redditApp implementation for Neo4j

Folder consists of three files: 
1. import.cipher - cipher script for import of the reddit data
2. redditApp.py - simple CLI application (Python script) - allows to run each of 8 app queries separately or do the benchmark run (6 repetitions of each query, timed and averaged, omitting the first run)
3. redditApp_data.zip - reddit data files (separate nodes and edges files). Data was originaly taken from Stanford Network Analysis Platform (SNAP): https://snap.stanford.edu/data/soc-RedditHyperlinks.html and preprocessed locally.

### redditApp setup

1. Create Neo4j database. For the project purposes all databases has been created in Neo4J Desktop tool.
2. Move reddit data (files 'nodes.csv' and 'title_relationships.csv') into the import folder.
3. Run import.cipher script
4. Run redditApp.py and follow the CLI menu
