#!/usr/bin/env bash
# Usage instructions:
# Modify all the paths here accordingly.
# Avoid using relative paths for safety.
# Execute `./run_all.sh <SF>` from inside the `scripts` folder.
# <SF> is the scale factor used to run the tests.

set -eu

# Check if exactly 2 arguments are provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <SCALE_FACTOR> <NUM_RUNS>"
  exit 1
fi

SCALE_FACTOR="$1"
NUM_RUNS=${2}

ROOT_PATH=$(wslpath "D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/orientdb-community-3.2.25/databases")
QUERY_FILES_PATH=$(wslpath "D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/orientdb-community-3.2.25/databases/queries")
PARAMETER_FILES_PATH=$(wslpath "D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/orientdb-community-3.2.25/databases/social_network-csv_merge_foreign-sf${SCALE_FACTOR}/substitution_parameters")

# definig the whole process by iteration
# python3 ./create_n_load.py -rp ${ROOT_PATH} -sf ${SCALE_FACTOR}
for ((i = 1; i<=${NUM_RUNS}; i++)); do
python3 ./ldbc.py -rp ${ROOT_PATH} -qp ${QUERY_FILES_PATH} -sf ${SCALE_FACTOR} -sp ${PARAMETER_FILES_PATH}
done