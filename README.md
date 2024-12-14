# MLOps project

## Project description

This project is a simple workflow to demonstrate learning about MLOps. It will use Airflow to orchestrate the training of a Yolo model with simulated continuous leaning.

![diag](images/project-diagram.png)

## Installation

### Option 1: Install with Flexible Dependencies
This method installs the project using the dependencies specified in `pyproject.toml`, allowing `pip` to resolve the latest compatible versions.

1. **Clone the Repository**:
2. **Install the requirements**:

   ```bash
   pip install .
   ```

### Option 2: Install with Exact Versions (Recommended for Production)

For a consistent environment with exact dependency versions, use the `requirements.txt` file.

1. **Install from `requirements.txt`**:

   ```bash
   pip install -r requirements.txt
   ```

## Adding Dependencies

To add or update dependencies in your project, follow these steps:

1. **Edit `pyproject.toml`**:
   Open the `pyproject.toml` file and add the new dependency under the `dependencies` section. For example:

   ```toml
   [project]
   dependencies = [
       "numpy>=1.21.0",
       "pandas>=1.3.0",
       "new-package>=1.0.0"
   ]
   ```

2. **Install the New Dependency**:
   Run the following command to install the new or updated dependency:

   ```bash
   pip install .
   ```

3. **Update `requirements.txt`** (Optional but Recommended):
   To lock the current versions of all dependencies for consistency, update `requirements.txt` by running:

   ```bash
   pip freeze > requirements.txt
   ```

### Start the Airflow docker image

mettre tout les packages dans le requirements.txt lors du build de l'image docker
l'image aura tout les packages necessaires pour lancer les dags

```bash
cd ./airflow
docker-compose up --build -d
# docker-compose up flower # start airflow and flower monitoring platform 
```

ou pour la nouvelle CLI de docker-compose
```bash
cd ./airflow
docker compose up --build -d
```

Then you can access the Airflow UI at http://localhost:8080/  
Then you can access the Flower UI at http://localhost:5555/  

### Stop and clean all
Pour stopper tout les containers et clean les images et les volumes:

```bash
cd ./airflow
docker compose down --volumes --rmi all
```

Stoper le container `bentoml_yolo_v8` s'il run toujous :

```bash
docker stop bentoml_yolo_v8
docker rm bentoml_yolo_v8
```

Vérifiez si l'image `yolo_v8:latest` existe encore, si oui supprimez là :

```bash
docker ps
docker rmi yolo_v8:latest
```

### Troubleshoothing
#### Linux
`Sous Linux` : il peut être nécessaire de changer la variable `AIRFLOW_UID` qui se trouve dans `airflow/.env`. Il faut également créer les répertoires de base pour en être propriétaire s'ils n'existent pas déjà :
```bash
cd ./airflow
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

Si l'erreur `Error: [bentoml-cli] containerize failed: Backend docker is not healty` survient dans la tache `containerize_bentoml` il faut décommenter la ligne `group_add` dans le `docker-compose.yaml` et ajouter le numéro du groupe docker de votre system `cat /etc/group | grep docker`. Cela va vous donner une ligne sous la forme `docker:x:###:mon-user`, `###` est le numéro de groupe.

#### Windows
`Sous Windows` : si une erreur survient dans la `pipeline_serve` au moment de containerize l'image sur le script `setup.sh` :
```bash
cd ./airflow/bentoml
dos2unix setup.sh
```

### Create the first DAG

Inside the dags folder you can create the py files that define the DAGs. Then refresh the Airflow UI and you will see the DAGs there.

```python
import pendulum

from airflow.decorators import task
from airflow.models import DAG
from airflow.operators.empty import EmptyOperator

dag = DAG(
    dag_id="branch_hello_world",
    schedule="@once",
    start_date=pendulum.datetime(2024, 11, 12, tz="UTC"),
)

run_this_first = EmptyOperator(task_id="run_this_first", dag=dag)


@task.branch(task_id="branching")
def do_branching():
    return "branch_a"


branching = do_branching()

branch_a = EmptyOperator(task_id="branch_a", dag=dag)
follow_branch_a = EmptyOperator(task_id="follow_branch_a", dag=dag)

branch_false = EmptyOperator(task_id="branch_false", dag=dag)

join = EmptyOperator(task_id="join", dag=dag)

run_this_first >> branching
branching >> branch_a >> follow_branch_a >> join
branching >> branch_false >> join
```

### Debug Airflow inside docker container using PyCharm
https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#debug-airflow-inside-docker-container-using-pycharm

## Airflow useful links
https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/datasets.html

## Data

https://www.mapillary.com/datasets

## Presentation on Airflow

https://docs.google.com/presentation/d/1-wukqNc3vpEbHzBJVt9H14qNZzdjb8Dl9J3qQs1SSvE/edit?usp=sharing
