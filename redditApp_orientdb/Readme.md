################################ Welcome to Reddit App ######################################

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
