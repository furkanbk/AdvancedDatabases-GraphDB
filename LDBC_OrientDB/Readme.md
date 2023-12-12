# Setting Up OrientDB for LDBC SNB Benchmark Results

1. **Download OrientDB Source File:**
   - Download the OrientDB source file from the official website using the following link: [OrientDB Community 3.2.25](https://repo1.maven.org/maven2/com/orientechnologies/orientdb-community/3.2.25/orientdb-community-3.2.25.zip)

2. **Run OrientDB Server:**
   - Extract the downloaded zip file.
   - Navigate to the `bin` folder and run the OrientDB server using the command `./server.sh`.
   - On the first run, create a username and password for future database operations.

3. **Access OrientDB Console:**
   - Run the console using `./console.sh` in the `bin` folder.
   - Connect to a database and execute queries.

4. **Reproduce Results:**
   - Copy contents from `LDBC_orientdb` folder to the `databases` folder in OrientDB.

5. **Download JDBC Drivers:**
   - Download JDBC drivers for your PostgreSQL version from [jdbc.postgresql.org](https://jdbc.postgresql.org).
   - Place the drivers in the `plugins` and `lib` folders of OrientDB.

6. **Teleporter Setup:**
   - Find teleporter scripts in the `Scripts` folder and teleporter drivers in the `Drivers` folder.
   - Place scripts in the `bin` folder and copy drivers into the `plugins` and `lib` folders of OrientDB.

Now, the environment is ready to reproduce the results.

7. **Run Teleporter**
Go to the `bin` folder and use the script:
```bash
./oteleporter.sh -jdriver <jdbc-driver> -jurl <jdbc-url> -juser <username> 
                -jpasswd <password> -ourl <orientdb-url> [-s <strategy>]
                [-nr <name-resolver>] [-v <verbose-level>] 
                ([-include <table-names>] | [-exclude <table-names>]) 
                [-inheritance <orm-technology>:<ORM-file-url>] 
                [-conf <configuration-file-location>]
```
To import your PostgreSQL database into OrientDB, follow these steps. It's straightforward; all you need to do is gather the correct JDBC driver for your PostgreSQL version. An example usage is shown below:

```bash
./oteleporter.sh -jdriver postgresql -jurl jdbc:postgresql://localhost:5432/testdb 
                -juser username -jpasswd password -ourl plocal:$ORIENTDB_HOME/databases/testdb 
                -s naive -nr java -v 1
```

# Benchmarking LDBC Database in OrientDB

8. Using the teleporter, you have now imported the LDBC database into OrientDB for all scale factors, and we can start benchmarking the results.

9. Go into the `database` folder and use the script `benchmark.sh` with the scale factor and number of runs to run the benchmark on a specified scale factor and for the desired number of iterations. Example usage:

   ```bash
   ./benchmark.sh <SCALE_FACTOR> <NUM_RUNS>
   ```
**Note:**
Before running the benchmark script, make sure to update the file locations. Specify the following paths in the benchmark shell script:

- `ROOT_PATH`: The root path for the benchmark.
- `QUERY_FILE_PATH`: The path where you copied the `Queries` folder.
- `PARAMETER_FILE_PATH`: The path where you have the substitution parameters.

10. After updating these paths, run the benchmark script for your desired scale factor and number of runs. This will generate benchmark results for the LDBC database, including CSV and text files with the logged timings for the OrientDB database.

**Important:** Ensure that you have the correct versions of JDBC drivers installed. Also, make sure that all plugins, lib, and scripts are in the right place, as mentioned above, to accurately reproduce the benchmark. 
