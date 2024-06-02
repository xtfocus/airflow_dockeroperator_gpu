# Airflow docker image to orchestrate the zalo prediction task

This is an Airflow docker image. To use it:
- clone this repo
- Initialize
```bash
docker compose up airflow-init
```
- Start containers
```bash
docker compose up -d # or without -d but in a tmux session so you can resume later and view logs
```
The main assesst of this repo is the DAG defined in `docker_operator_example.py`. This DAG uses the image described in [another repo](https://github.com/xtfocus/zalo_negoos_daily_docker_operator)
