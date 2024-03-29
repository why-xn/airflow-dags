from datetime import datetime, timedelta
import random
import math
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from kubernetes.client import models as k8s
from airflow.utils.dates import days_ago

# Define default_args dictionary to pass to the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
}

# Instantiate a DAG
dag = DAG(
    'hello_k8_dag',
    default_args=default_args,
    description='A simple Airflow DAG with KubernetesExecutor',
    schedule_interval=None,
    catchup=False,
    max_active_runs=2
)

# Define a Python function to be executed by the task
def print_hello():
    print("Hello, Kubernetes!")

def  estimate_pi():
    num_points = 1000000
    points_inside_circle = 0

    for _ in range(num_points):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)

        distance = math.sqrt(x**2 + y**2)

        if distance <= 1:
            points_inside_circle += 1

    pi_estimate = (points_inside_circle / num_points) * 4
    
    print("Calculated pi:")
    print(pi_estimate)

start_task = DummyOperator(task_id='start', dag=dag)
end_task = DummyOperator(task_id='end', dag=dag)

# Create a task using the PythonOperator
task_hello = PythonOperator(
    task_id='print_hello_task',
    python_callable=print_hello,
    dag=dag,
)

# Create a task using the PythonOperator
task_pi = PythonOperator(
    task_id='estimate_pi_task',
    python_callable=estimate_pi,
    dag=dag,
)

# Set task dependencies
start_task >> task_hello >> end_task
start_task >> task_pi >> end_task

