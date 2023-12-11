#!/usr/bin/env bash
# Usage instructions:
# Modify all the paths here accordingly.
# Avoid using relative paths for safety.
# Execute `./run_all.sh <SF>` from inside the `scripts` folder.
# <SF> is the scale factor used to run the tests.

set -eu

# Check if exactly 1 argument is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <SCALE_FACTOR>"
  exit 1
fi

SCALE_FACTOR="$1"

# Paths
ROOT_PATH=$(wslpath "D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/orientdb-community-3.2.25/databases")
CSV_FILE_PATH=$(wslpath "D:/BDMA/ULB_COURSES/ADVANCED_DATABASES/project/orientdb-community-3.2.25/databases/data")

# Variables
DATABASE_NAME="reddit_db_sf_${SCALE_FACTOR}"
USERNAME="root"
PASSWORD="root"
SCRIPT_PATH="load_reddit_db_${SCALE_FACTOR}.osql"

# OrientDB commands
CREATE_DB_COMMAND="create database remote:localhost/${DATABASE_NAME} root root"
CONNECT_COMMAND="connect remote:localhost/${DATABASE_NAME} ${USERNAME} ${PASSWORD}"
LOAD_SCRIPT_COMMAND="LOAD SCRIPT ${SCRIPT_PATH}"

# run the python script
python3 ./orientdb_data_gen.py -rp "${ROOT_PATH}" -fp "${CSV_FILE_PATH}" -sf "${SCALE_FACTOR}"

# Run OrientDB commands
../bin/console.sh <<-EOF
  ${CREATE_DB_COMMAND};
  ${CONNECT_COMMAND};
  ${LOAD_SCRIPT_COMMAND};
  exit;
EOF