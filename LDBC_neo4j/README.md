# LDBC SNB Benchmark implementation for Neo4j

Folder consists of four files: 
1. ldbc_import.cipher - cipher script for import of the SNB data
2. benchmark_run.py - Python script for running benchmark - each of the 14 complex queries in the benchmark are executed 6 times and final averaged time of each query is taken from the 5 runs (omitting the first run)
3. ldbc_snb_datasf0.1.zip - SNB data for Scale Factor 0.1. Data can be accessed from the webpage: https://ldbcouncil.org/data-sets-surf-repository/snb-interactive-v1-datagen-v100.html (SNB Interactive v1: CsvComposite serializer using LongDateFormatter)
4. substitution_parameters_sf0.1zip - substitution parameters for Scale Factore 0.1 . Can be accessed from the same webpage: https://ldbcouncil.org/data-sets-surf-repository/snb-interactive-v1-datagen-v100.html (SNB Interactive v1: Substitution parameters)

### ⚠️ Warning ⚠️

Pregenerated data webpage is constantly changing - most current update was on 10.12.2023. For this reason links for data access might not be up-to-date on upcoming days. General repository where the data can be found is: https://github.com/ldbc/data-sets-surf-repository

### Benchmark step-by-step

1. Create Neo4j database. For the project purposes all databases has been created in Neo4J Desktop tool.
2. Move benchmark data (folders 'static' and 'dynamic') into the import folder.
3. Run ldbc_import.cipher script
4. Specify substitution_parameter_directory in benchmark_run.py and run the script
