# OrientDB RedditApp Setup Guide

![OrientDB_Org](https://github.com/Reitnos/AdvancedDatabases-GraphDB/assets/68030078/0ca50065-d5c8-4477-b513-299476f8462a)

## Introduction

Welcome to the OrientDB RedditApp Setup Guide! This guide will walk you through the process of setting up OrientDB for the RedditApp, including downloading the source file, running the OrientDB server, and reproducing the results.

## Setup Steps

### Step 1: Download OrientDB

Download the OrientDB source file from the official OrientDB website using the following link: [Download OrientDB 3.2.25](https://repo1.maven.org/maven2/com/orientechnologies/orientdb-community/3.2.25/orientdb-community-3.2.25.zip)

### Step 2: Extract and Run OrientDB Server

1. Extract the downloaded zip folder.
2. Navigate to the `bin` folder and run the OrientDB server using the command:

    ```bash
    ./server.sh
    ```

    On the first run, you will be prompted to create a username and password. These credentials will be used when creating further databases.

### Step 3: Access OrientDB Console

Run the OrientDB console using the command:

```bash
./console.sh
```
### Step 4: Reproduce Results for RedditApp

1. Copy the contents of the `redditApp_orientdb` folder into the `databases` folder of the downloaded OrientDB.

2. Navigate to the `Load_data` folder and run the create database shell script:

    ```bash
    ./create_db.sh <scale_factor>
    ```

    Replace `<scale_factor>` with the desired number of edges. For example, running `./create_db.sh 1000` will create a Reddit database with 1000 edges.

    **Note:** Adjust file path parameters in the shell script according to your local file paths, and provide the necessary username, password, and database name.

3. After running the script, the schema and data for the specified scale factor will be created.

### Conclusion

Congratulations! You have successfully set up OrientDB for the RedditApp. Feel free to explore the database and analyze the results.

For more information and documentation, visit the [OrientDB Official Documentation](https://orientdb.org/docs/3.2.x/).

---

*Disclaimer: This guide assumes basic knowledge of OrientDB and database concepts. Please refer to the official documentation for detailed information.*

The default database for the queries is named "reddit_db_100k" in main.py
If you have a different name for your database (probably a different scale factor)
please change it accordingly.

Database creation for the app: We provide a .osql file and a shell script to load the 
data into the OrientDB database.

First create an empty database named "reddit_db_100k" 

Specify the path of the .osql file inside the shell script and then run it.

Database connection: main.py uses RestAPI to connect to OrientDB database. User needs
to enter their own host,username,password information in the relevant places.

You need to have OrientDB server running in order to connect and query the server through
this game. For this, go to OrientDB bin folder and do "/server.sh"

Run main.py and follow the instructions on terminal, Enjoy!
