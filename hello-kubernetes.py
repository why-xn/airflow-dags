from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Define default_args dictionary to pass to the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False
}

# Instantiate a DAG
dag = DAG(
    'hello_kubernetes_dag',
    default_args=default_args,
    description='A simple Airflow DAG with KubernetesExecutor',
)

# Define a Python function to be executed by the task
def print_hello():
    print("Hello, Kubernetes!")

# Create a task using the PythonOperator
task_hello = PythonOperator(
    task_id='print_hello_task',
    python_callable=print_hello,
    dag=dag,
)

# Set task dependencies
task_hello

