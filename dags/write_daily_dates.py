from airflow.decorators import dag, task
from airflow.models import Variable
from pendulum import datetime


@dag(
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["activity"],
)
def write_date():

    @task
    def get_date(**kwargs):

        today = kwargs.get("ds")

        return today

    @task
    def write_date_to_file(response):

        filepath = Variable.get(
            "activity_file"
        )  # https://marclamberti.com/blog/variables-with-apache-airflow/

        with open(filepath, "a") as f:

            f.write(f"{response}\r\n")

        return filepath

    @task
    def read_activity_from_file(filepath):

        with open(filepath, "r") as h:

            print(h.read())

    response = get_date()

    read_activity_from_file(write_date_to_file(response))


write_date()
