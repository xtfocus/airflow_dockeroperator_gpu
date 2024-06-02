from airflow.decorators import dag, task
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount, DeviceRequest
from pendulum import datetime


@dag(start_date=datetime(2024, 1, 1), schedule="@daily", catchup=False, max_active_runs=1)
def docker_dag():

    @task
    def t1(**kwargs):
        date = kwargs.get("ds")
        return date

    t2 = DockerOperator(
        task_id="t2",
        image="kedro-docker:v1",
        # command="python3 app.py",
        command="sh -c 'export DAY_REQUEST={{ ds }} && echo $DAY_REQUEST && kedro run'",
        device_requests=[DeviceRequest(count=-1, capabilities=[['gpu']])],
        #command=f"echo 'command is running in the docker container'",
        # https://stackoverflow.com/questions/61186983/airflow-dockeroperator-connect-sock-connectself-unix-socket-filenotfounderror/71853705#71853705
        # chmod 666 this shit
        docker_url="unix://var/run/docker.sock",
        # other suggests https://stackoverflow.com/a/70100729/10468347
        network_mode="bridge",
    )

    t1() >> t2


docker_dag()
