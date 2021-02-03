from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
   'owner': 'Aluizio Cidral Júnior',
   'depends_on_past': False,
   'start_date': days_ago(2),
   'retries': 1,
   }

with DAG(
   'DAG',
   schedule_interval=timedelta(days=1),
   default_args=default_args
   ) as dag:

   t1 = BashOperator(
   task_id='1_etl',
   bash_command="""
   cd $AIRFLOW_HOME/dags/tasks/
   python3 task1.py {{ execution_date }}
   """)
   
   t2 = BashOperator(
   task_id='2_etl',
   bash_command="""
   cd $AIRFLOW_HOME/dags/tasks/
   python3 task2.py {{ execution_date }}
   """)

   t3 = BashOperator(
   task_id='3_etl',
   bash_command="""
   cd $AIRFLOW_HOME/dags/tasks/
   python3 task3.py {{ execution_date }}
   """)

[t1,t2] >> t3