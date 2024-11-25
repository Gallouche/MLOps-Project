# MLOps project

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

```bash
cd ./airflow
docker-compose up
# docker-compose up flower # start airflow and flower monitoring platform 
```

Then you can access the Airflow UI at http://localhost:8080/  
Then you can access the Flower UI at http://localhost:5555/  

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