# 🚀 Technical Challenge — Data Pipeline with Meltano and Airflow

This project implements a data pipeline using Meltano for extraction and transformation, and Apache Airflow for orchestration.


## 📌 Objective

Build a pipeline that:

- Extracts data from:

    - CSV file

    - PostgreSQL database

    - Transforms and saves the data in Parquet format

    - Loads the processed data into a PostgreSQL database

    - Orchestrates all steps using Apache Airflow


## 🛠️ Technologies Used

- Meltano

- Apache Airflow

- Python (for loading script)

- PostgreSQL

- Docker

## 📂 Pipeline Structure

- Step 1 (ETL with Meltano)

    - tap-csv → target-parquet

    - tap-postgres → target-parquet

- Step 2 (Loading to database)

    - Reads Parquet files

    - Loads data into PostgreSQL using a Python script (parquet_to_db.py)

- Orchestration with Airflow

    - DAG meltano_daily_etl created with all 3 steps

    - Scheduled to run daily at midnight

⚠️ Note: Airflow is configured in the project, but due to an issue in the docker-compose.yml, the final execution was performed manually. The DAG is fully functional and ready for execution in a working Airflow environment.

## 🧠 What I Learned

- How to integrate Meltano with multiple data sources

- Efficient conversion of data to Parquet format

- Creation of automated pipelines with Airflow

- Using Python scripts as flexible alternatives for specific tasks

## 🚧 How to Run the Project

```
# Install dependencias
pip install -r requirements.txt

# Start the PostgreSQL database 
docker-compose up -d

# Install Meltano dependencies
cd meltano
meltano install

# Run the Meltano pipelines manually
meltano run tap-csv target-parquet
meltano run tap-postgres target-parquet

# Run the Python script to load Parquet data into PostgreSQL
python3 parquet_to_db.py
```
