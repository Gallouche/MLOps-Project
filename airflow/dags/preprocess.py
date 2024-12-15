from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

from src.preprocessing.gcs_download import download_and_delete_files_from_gcs
from src.preprocessing.parse_annotations import convert_all_to_yolo
from src.preprocessing.gcs_upload import split_data, upload_new_data

SERVICE_ACCOUNT_JSON_DOWNLOAD = "./dags/drop-bucket-key.json"
SERVICE_ACCOUNT_JSON_UPLOAD = "./dags/mse-machledata-key.json"
DATASET_FOLDER = "tmp/"


# def list_files():
#     for root, _, files in os.walk(DATASET_FOLDER):
#         for file in files:
#             print("File: ", os.path.join(root, file))


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
        op_kwargs={"SERVICE_ACCOUNT_JSON": SERVICE_ACCOUNT_JSON_DOWNLOAD},
    )

    convert_all_to_yolo_task = PythonOperator(
        task_id="convert_all_to_yolo",
        python_callable=convert_all_to_yolo,
        op_kwargs={"json_directory": DATASET_FOLDER + "annotations",
                   "output_directory": DATASET_FOLDER + "annotations_yolo/"},
    )

    list_files_task = PythonOperator(
        task_id="list_files",
        python_callable=list_files,
    )

    split_data_task = PythonOperator(
        task_id="split_data",
        python_callable=split_data,
        op_kwargs={"local_folder": DATASET_FOLDER},
    )

    upload_new_data_task = PythonOperator(
        task_id="upload_new_data",
        python_callable=upload_new_data,
        op_kwargs={"SERVICE_ACCOUNT_JSON": SERVICE_ACCOUNT_JSON_DOWNLOAD}
    )

    # Set task dependencies
    download_and_delete_task >> convert_all_to_yolo_task >> split_data_task >> upload_new_data_task
