import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta

from dag_functions.functions import AWS_Airflow


dag_functions=AWS_Airflow()

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(0),
}

dag = DAG(
    dag_id='projeto_final_bootcamp'
    , default_args=args
    ,schedule_interval=None
    ,dagrun_timeout=timedelta(minutes=60)
)

t1 = PythonOperator(
    task_id='leitura_secret_manager'
    ,python_callable=dag_functions.get_secret
    ,dag=dag
)

t2 = PythonOperator(
    task_id='obter_token_api_embrapa'
    ,python_callable=dag_functions.get_token
    ,op_args=[t1.output]
    ,dag=dag
)

t3 = PythonOperator(
    task_id='coleta_dados_embrapa'
    ,python_callable= dag_functions.get_embrapa_data
    ,op_args=[t2.output]
    ,dag=dag
)

t4 = PythonOperator(
    task_id='escreve_dados_s3'
    ,python_callable= dag_functions.write_data_s3
    ,op_args=[t3.output]
    ,dag=dag
)


t1 >> t2 >> t3 >> t4