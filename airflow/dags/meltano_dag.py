from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import BashOperator, PythonOperator
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
meltano_dir = os.path.join(current_dir, '../meltano') 
load_dir = os.path.join(meltano_dir, 'load') 

sys.path.append(meltano_dir)

from parquet_to_db import load_nested_parquet_to_db

def print_success_message(task_name, **kwargs):
    print(f"Tarefa '{task_name}' concluída com sucesso!")

default_args = {
    'owner': 'Adriel',
    'start_date': datetime(2023, 10, 4),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'meltano_daily_etl',
    default_args=default_args,
    description='Pipeline diário com múltiplos passos Meltano',
    schedule_interval='0 0 * * *', 
    catchup=False,
)

# Tasks

el_postgres_parquet = BashOperator(
    task_id='extract_data',
    bash_command='cd meltano && meltano run tap-postgres target-parquet',
    dag=dag,
)

success_postgres = PythonOperator(
    task_id='success_postgres',
    python_callable=print_success_message,
    op_kwargs={'task_name': 'extract_postgres_to_parquet'},
    dag=dag,
)


el_csv_parquet = BashOperator(
    task_id='extract_data',
    bash_command='cd meltano && meltano run tap-csv target-parquet',
    dag=dag,
)

success_csv = PythonOperator(
    task_id='success_csv',
    python_callable=print_success_message,
    op_kwargs={'task_name': 'extract_csv_to_parquet'},
    dag=dag,
)

el_parquet_posgres = PythonOperator(
    task_id='load_data',
    python_callable=load_nested_parquet_to_db,
    op_kwargs={
        'engine': 'postgresql://northwind:northwind@localhost/northwind',
        'base_path': load_dir,
    },
    dag=dag,
)

success_step_2 = PythonOperator(
    task_id='success_load',
    python_callable=print_success_message,
    op_kwargs={'task_name': 'load_parquet_to_postgres'},
    dag=dag,
)
el_postgres_parquet >> success_postgres
el_csv_parquet >> success_csv
[success_postgres, success_csv] >> el_parquet_posgres >> success_step_2