from airflow.models.dag import DAG
from datetime import timedelta, datetime
from airflow.operators.bash import BashOperator

with DAG(
    "tutorial",
    default_args={},
    description="dag tutorial",
    schedule=timedelta(minutes=60),
    start_date=datetime(2024, month=12, day=2),
    tags=["my_dag"]

) as dag:
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date"
    )

    t1