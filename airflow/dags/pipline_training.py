from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from google.cloud import storage
import os
import yaml
from ultralytics import YOLO

# Constants
BUCKET_NAME = "mse_mapillary"
DATASET_FOLDER = "/tmp"
SERVICE_ACCOUNT_JSON = "./dags/mse-machledata-key.json"

DEPENDENCY_DAG_ID="serve_pipeline"
DEPENDENCY_TASK_ID="containerize_bentoml"

# Authentication setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_JSON

def download_data_from_gcs(**kwargs):
    """Download data from Google Cloud Storage."""
    print("OS.ENVIORENEMENT: ", os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    # print file in the current directory
    print(os.listdir())
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
    bucket = client.get_bucket(BUCKET_NAME)
    blobs = bucket.list_blobs()  # Adjust your prefix
    os.makedirs(DATASET_FOLDER, exist_ok=True)
    
    # Save the blobs as files with the same structure as in the bucket
    for blob in blobs:
        print(blob.name)
        os.makedirs(os.path.join(DATASET_FOLDER, os.path.dirname(blob.name)), exist_ok=True)
        blob.download_to_filename(os.path.join(DATASET_FOLDER, blob.name))

def print_folder_content(**kwargs):
    """Print the content of the dataset folder."""
    print(os.listdir(DATASET_FOLDER))

def train_yolov8_model(**kwargs):
    """Train YOLOv8n model."""
    model = YOLO("yolov8n.pt")  # Load YOLOv8n
    results = model.train(
        data=os.path.join("./dags/dataset.yaml"),  # Your dataset config
        epochs=1,
        imgsz=640,
        batch=2,
        workers=1
    )

def upload_to_gcs(**kwargs):
    """Upload the trained model and metrics to Google Cloud Storage."""
    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)

    # Upload all the data inside the ./runs/detect/train folder to GCS under the name "trained_model" and subfolders
    for root, _, files in os.walk("./runs/detect/train"):
        for file in files:
            
            if os.path.relpath(root, './runs/detect/train') == ".":  # If the root is the current directory
                print(f"Uploading {os.path.join(root, file)} to trained_model/{file}")
                blob = bucket.blob(f"trained_model/{file}")
            else:
                print(f"Uploading {os.path.join(root, file)} to trained_model/{os.path.relpath(root, './runs/detect/train')}/{file}")
                blob = bucket.blob(f"trained_model/{os.path.relpath(root, './runs/detect/train')}/{file}")
            blob.upload_from_filename(os.path.join(root, file))

# Default arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(minutes=60),
}

# DAG definition
with DAG(
    "yolov8_training_pipeline",
    default_args=default_args,
    description="A DAG to train YOLOv8n on GCS data and upload results",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["yolo", "training", "gcs"],
) as dag:
    
    download_task = PythonOperator(
        task_id="download_data_from_gcs",
        python_callable=download_data_from_gcs ,
    )

    remove_train_output = BashOperator(
        task_id="remove_train_output",
        bash_command="rm -rf /opt/airflow/runs",
    )

    train_task = PythonOperator(
        task_id="train_yolov8_model",
        python_callable=train_yolov8_model,
    )

    upload_task = PythonOperator(
        task_id="upload_to_gcs",
        python_callable=upload_to_gcs,
    )

    trigger_other_dag = TriggerDagRunOperator(
      task_id='trigger_deployement',
      trigger_dag_id=DEPENDENCY_DAG_ID,
      wait_for_completion=False, 
      reset_dag_run=True,
      dag=dag,
    )

download_task >> remove_train_output >> train_task >> upload_task >> trigger_other_dag