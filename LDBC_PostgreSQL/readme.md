# Setting Up LDBC SNB Interactive V1 Benchmark

1. **Clone the LDBC SNB Interactive V1 Implementation:**
   - Clone the LDBC SNB Interactive V1 implementation from the GitHub repository: [LDBC SNB Interactive V1 Implementations](https://github.com/ldbc/ldbc_snb_interactive_v1_impls/tree/main)

2. **Copy PostgreSQL Implementation Contents:**
   - Navigate into the `postgres` folder and copy the contents from the `LDBC_PostgreSQL` folder into the cloned repository.

3. **Download LDBC Benchmark Data:**
   - Download the LDBC benchmark data for different scale factors using the [LDBC SNB Surf Repository](https://ldbcouncil.org/data-sets-surf-repository/snb-interactive-v1-datagen-v035.html). Utilize the SNB Interactive V1: CsvCompositeMergeForeign serializer using StringDateFormatter files for scale factors 0.1, 0.3, 1, and 3.

4. **Replace DDL Folder and Update Paths:**
   - Replace the `ddl` folder in the repository with the `ddl` folder from the `LDBC_PostgreSQL` folder.
   - Update folder paths in the `load_sf<SCALE_FACTOR>.sql` files to indicate the location of the downloaded LDBC data for loading.

5. **Copy Substitution Parameters and Queries:**
   - Copy the substitution parameters folder into the repository.
   - Copy the substitution parameter for a scale factor to its data folder so that it can be used in the benchmark for replacing the placeholders in the queries.

# PostgreSQL Benchmark Setup for LDBC SNB Interactive V1 Benchmark
**Note:**
Ensure to follow these steps for a successful PostgreSQL benchmark setup:

6. **Organize Scripts:**
   - Place the `create_n_load.py`, `power_test.py`, and `benchmark.sh` in the PostgreSQL scripts folder. This is essential for the benchmark script to locate the required Python files.

7. **Configuration Parameters:**
   - Remember to adjust the following configuration parameters in the benchmark setup:
     - `ROOT_PATH`: The root path for the benchmark.
     - `QUERY_FILES_PATH`: Folder path where the queries are stored.
     - `PARAMETER_FILES_PATH`: Folder path, according to the scale factor, where the substitution parameters are stored.

8. **Run Benchmark:**
   - After organizing the scripts and configuring the parameters, run the benchmark script for your desired scale factor and number of runs. Example usage:

     ```bash
     ./benchmark.sh <SCALE_FACTOR> <NUM_RUNS>
     ```

9. **Benchmark Results:**
   - After running the benchmark script, it will generate benchmark results for the LDBC database. These results will include CSV and text files with the logged timings specifically for the PostgreSQL database.