#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define paths
SCRIPT_PATH="extract/update_column_types.py"

# Step 1: Run the Python script to update column types
echo "Running update_column_types.py..."
python3 "$SCRIPT_PATH"

# Step 2: Install Meltano plugins
echo "Installing Meltano plugins..."
meltano install

# Step 3: Run the Meltano pipeline
echo "Running Meltano pipeline..."
meltano run tap-postgres target-parquet

echo "Pipeline execution completed successfully!"