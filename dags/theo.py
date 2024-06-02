from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# Function to write the current execution date to a file


def write_date_fn(thing):
    with open("/tmp/dates.txt", "a") as file:
        file.write(f"{thing}_thingy" + "\n")


def read_file_fn():
    with open("/tmp/dates.txt", "r") as file:
        print(file.read())


# Define the DAG

with DAG(
    "yo_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # Define the PythonOperator

    write_date_task = PythonOperator(
        task_id="write_date", python_callable=write_date_fn, op_args=["{{ ds }}"]
    )
    read_task = PythonOperator(
        task_id="read_file",
        python_callable=read_file_fn,
    )

    # Set the task in the DAG
    write_date_task >> read_task
