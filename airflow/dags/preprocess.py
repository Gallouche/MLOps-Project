from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from src.gcs import download_and_delete_files_from_gcs
from src.parse_annotations import convert_all_to_yolo

SERVICE_ACCOUNT_JSON = "./dags/drop-bucket-key.json"
DATASET_FOLDER = "tmp/"

# Define the DAG
with DAG(
    dag_id="download_and_process_files_from_gcs",
    start_date=datetime(2024, 12, 12),
    schedule_interval=None,  # Run manually
    catchup=False,
) as dag:

    download_and_delete_task = PythonOperator(
        task_id="download_and_delete_files",
        python_callable=download_and_delete_files_from_gcs,
        op_kwargs={"SERVICE_ACCOUNT_JSON": SERVICE_ACCOUNT_JSON},
    )

    convert_all_to_yolo_task = PythonOperator(
        task_id="convert_all_to_yolo",
        python_callable=convert_all_to_yolo,
        op_kwargs={"json_directory": DATASET_FOLDER + "annotations",
                   "output_directory": DATASET_FOLDER + "annotations_yolo/"},
    )

    # Set task dependencies
    download_and_delete_task >> convert_all_to_yolo_task
