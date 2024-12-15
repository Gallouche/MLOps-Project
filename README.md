# MLOps project

## Project description

This project is a simple workflow to demonstrate learning about MLOps. It will use Airflow to orchestrate the training of a Yolo model with simulated continuous leaning.

![diag](images/project-diagram.png)

### Docker & Docker compose version

For the pipeline to run, you must have at least the following versions of docker

#### Windows

```bash
Docker version 26.1.1, build 4cf5afa
Docker Compose version v2.27.0-desktop.2
```

#### Linux

```bash
Docker version 27.3.1, build ce12230
Docker Compose version v2.29.7
```

### Start the Airflow docker image

Start the Airflow docker image with the following command:

```bash
cd ./airflow
docker-compose up --build -d
# docker-compose up flower # start airflow and flower monitoring platform
```

Or for the new docker-compose CLI

```bash
cd ./airflow
docker compose up --build -d
```

Then you can access the Airflow UI at http://localhost:8080/  
Then you can access the Flower UI at http://localhost:5555/

### Stop and clean all

For stop all containers and clean images and volumes:

```bash
cd ./airflow
docker compose down --volumes --rmi all
```

Stop the container `bentoml_yolo_v8` if it is still running:

```bash
docker stop bentoml_yolo_v8
docker rm bentoml_yolo_v8
```

Verify if the image `yolo_v8:latest` still exists, if so delete it:

```bash
docker ps
docker rmi yolo_v8:latest
```

### Troubleshoothing

#### Linux

`Under Linux` : it may be necessary to change the `AIRFLOW_UID` variable in `airflow/.env`. It is also necessary to create the basic directories to be the owner if they do not already exist:

```bash
cd ./airflow
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

If the error `Error: [bentoml-cli] containerize failed: Backend docker is not healty` occurs in the `pipeline_serve` in the `containerize_bentoml` task, you must uncomment the `group_add` line in the `docker-compose.yaml` and add the docker group number of your system `cat /etc/group | grep docker`. This will give you a line in the form `docker:x:###:my-user`, `###` is the group number.

#### Windows

`Under Windows` : if an error `INFO - #18 ERROR: process "/bin/sh -c /home/bentoml/bento/env/docker/setup_script" did not complete successfully: exit code: 127` occurs in the `pipeline_serve` in the `containerize_bentoml` task:

```bash
cd ./airflow/bentoml
dos2unix setup.sh
```

### Debug Airflow inside docker container using PyCharm

https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#debug-airflow-inside-docker-container-using-pycharm

## Airflow useful links

https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/datasets.html

## Data source

https://www.mapillary.com/datasets

## Presentation on Airflow

https://docs.google.com/presentation/d/1-wukqNc3vpEbHzBJVt9H14qNZzdjb8Dl9J3qQs1SSvE/edit?usp=sharing
