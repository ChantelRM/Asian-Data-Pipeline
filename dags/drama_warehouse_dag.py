"""
Airflow DAG: Asian Drama Analytics Warehouse.

YOUR TASK: wire up a DAG with one task per pipeline stage:
  extract_mydramalist, extract_tmdb, clean_dramas, load_dramas

THINK ABOUT (this is the actual orchestration design decision, not
boilerplate):
  - Which tasks can run in parallel, and which must run in sequence?
    (hint: does extract_tmdb need anything that comes out of
    extract_mydramalist? does clean_dramas need output from BOTH
    extracts before it can run?)
  - Should every task retry the same number of times with the same
    delay? Think about which stage is most likely to fail for reasons a
    retry would actually fix (a flaky third-party API call) versus a
    stage that would just fail the same way every time no matter how
    many times you retry it (a missing local file) — retrying the
    second kind just delays you discovering a config problem.
  - task_id naming, DAG-level default_args, schedule_interval (probably
    None / manual-trigger-only for a two-week project rather than a
    real cron schedule).

Import your four pipeline functions from src.extract / src.transform /
src.load, wrap each in a PythonOperator, and set the dependency
chain with >> operators (or a list like [task_a, task_b] >> task_c if
two tasks both need to finish before a third starts).
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

import sys
sys.path.insert(0, "/opt/airflow")

# TODO: import your four pipeline functions, e.g.:
# from src.extract.extract_mydramalist import extract_mydramalist
# from src.extract.extract_tmdb import extract_tmdb
# from src.transform.clean_dramas import clean_dramas
# from src.load.load_postgres import load_dramas

default_args = {
    "owner": "chantel",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 0,
}

with DAG(
    dag_id="asian_drama_warehouse",
    description="Extract, validate, clean, and load Asian drama data into the star schema warehouse",
    default_args=default_args,
    start_date=datetime(2026, 7, 1),
    schedule_interval=None,
    catchup=False,
    tags=["drama-warehouse", "portfolio"],
) as dag:

    # TODO: define one PythonOperator per pipeline stage:
    #   extract_mydramalist_task = PythonOperator(task_id=..., python_callable=...)
    #   extract_tmdb_task = PythonOperator(task_id=..., python_callable=..., retries=?, retry_delay=?)
    #   clean_dramas_task = PythonOperator(...)
    #   load_dramas_task = PythonOperator(...)

    # TODO: wire up the dependency chain with >> operators.
    pass
