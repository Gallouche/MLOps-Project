from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow import DAG
import os
from google.cloud import storage

# Constants
BUCKET_NAME = "mse_mapillary"
WEIGHTS_BLOB = "trained_model/weights/best.pt"
SERVICE_ACCOUNT_JSON = "/opt/airflow/dags/mse-machledata-key.json"
BENTOML_PATH = "/opt/airflow/bentoml"
LOCAL_WEIGHTS_PATH = "/opt/airflow/bentoml/best.pt"

# Authentication setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_JSON

def download_weights_from_gcs():
    """
    Télécharge un fichier depuis un bucket GCS.
    """
    print("OS.ENVIORENEMENT: ", os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    print("Téléchargement des poids depuis GCS...")
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(WEIGHTS_BLOB)
    blob.download_to_filename(LOCAL_WEIGHTS_PATH)
    print(f"Poids téléchargés depuis GCS et sauvegardés dans {LOCAL_WEIGHTS_PATH}")

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
    "serve_pipeline",
    default_args=default_args,
    description="A DAG to deploy the model with the best weights and serve with BentoML",
    schedule_interval=None,
    # start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["yolo", "deploy", "gcs", "bentoml", "serve"],
) as dag:
    
    download_weights_task = PythonOperator(
        task_id='download_weights_from_gcs',
        python_callable=download_weights_from_gcs,
        dag=dag,
    )

    build_bentoml_task = BashOperator(
        task_id='build_bentoml',
        bash_command=f'cd {BENTOML_PATH} && bentoml build',
        #bash_command='echo "Working directory: $(pwd)" && ls -l',
        dag=dag,
    )

    containerize_bentoml_task = BashOperator(
        task_id='containerize_bentoml',
        bash_command='bentoml containerize yolo_v8:latest',
        #bash_command='echo "Working directory: $(pwd)" && ls -l',
        dag=dag,
    )

    run_bentoml_container_task = DockerOperator(
        task_id='run_bentoml_container',
        image="yolo_v8:latest",
        auto_remove=True,  # Supprime automatiquement le container après exécution
        docker_url="unix://var/run/docker.sock",
        #docker_url='TCP://docker-socket-proxy:2375',
        network_mode="bridge",
        command="serve",
        port_bindings={"3000":3000},
        dag=dag,
    )

    download_weights_task >> build_bentoml_task >> containerize_bentoml_task >> run_bentoml_container_task