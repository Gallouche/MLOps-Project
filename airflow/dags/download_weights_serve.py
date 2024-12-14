from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow import DAG
import os
from google.cloud import storage
import subprocess

# Constants
DOCKER_CONTAINER_NAME = "bentoml_yolo_v8"
DOCKER_IMAGE_NAME = "yolo_v8:latest"
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

def check_bentoml_container():
    """
    Vérifie si le conteneur est actif et retourne l'ID de la branche appropriée.
    """
    print("Vérification du conteneur BentoML...")
    result = subprocess.run(
        ["docker", "ps", "-q", "-f", f"name={DOCKER_CONTAINER_NAME}"],
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        print(f"Conteneur {DOCKER_CONTAINER_NAME} trouvé. Arrêt nécessaire.")
        return "stop_bentoml_container"
    else:
        print(f"Conteneur {DOCKER_CONTAINER_NAME} non trouvé.")
        return "check_docker_image"
    
def check_docker_image():
    """
    Vérifie si une image Docker existe et retourne l'ID de la branche appropriée.
    """
    print(f"Vérification de l'image Docker '{DOCKER_IMAGE_NAME}'...")
    result = subprocess.run(
        ["docker", "images", "-q", DOCKER_IMAGE_NAME],
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        print(f"L'image Docker '{DOCKER_IMAGE_NAME}' existe.")
        return "rm_docker_image"
    else:
        print(f"L'image Docker '{DOCKER_IMAGE_NAME}' n'existe pas.")
        return "containerize_bentoml"

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

    check_bentoml_container_task = BranchPythonOperator(
        task_id="check_bentoml_container",
        python_callable=check_bentoml_container,
        dag=dag,
    )

    stop_bentoml_container_task = BashOperator(
        task_id="stop_bentoml_container",
        bash_command=f"docker stop {DOCKER_CONTAINER_NAME}",
        dag=dag,
    )

    check_docker_image_task = BranchPythonOperator(
        task_id="check_docker_image",
        trigger_rule='none_failed_or_skipped',
        python_callable=check_docker_image,
        dag=dag,
    )

    rm_docker_image_task = BashOperator(
        task_id="rm_docker_image",
        bash_command=f"docker rmi {DOCKER_IMAGE_NAME}",
        dag=dag,
    )

    containerize_bentoml_task = BashOperator(
        task_id='containerize_bentoml',
        trigger_rule='none_failed_or_skipped',
        bash_command=f'bentoml containerize yolo_v8:latest -t {DOCKER_IMAGE_NAME}',
        #bash_command='echo "Working directory: $(pwd)" && ls -l',
        dag=dag,
    )

    run_bentoml_container_task = DockerOperator(
        task_id='run_bentoml_container',
        image=f"{DOCKER_IMAGE_NAME}",
        auto_remove=True,  # Supprime automatiquement le container après exécution
        docker_url="unix://var/run/docker.sock",
        container_name=DOCKER_CONTAINER_NAME,
        #docker_url='TCP://docker-socket-proxy:2375',
        network_mode="bridge",
        command="serve",
        port_bindings={"3000":3000},
        dag=dag,
    )

    download_weights_task >> build_bentoml_task >> check_bentoml_container_task >> [stop_bentoml_container_task, check_docker_image_task]
    stop_bentoml_container_task >> check_docker_image_task >> [rm_docker_image_task, containerize_bentoml_task]
    rm_docker_image_task >> containerize_bentoml_task
    containerize_bentoml_task >> run_bentoml_container_task