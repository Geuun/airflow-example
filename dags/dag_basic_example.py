from datetime import datetime, timedelta
from textwrap import dedent

# DAG 객체로써 DAG를 인스턴스화 하는데 필요합니다.
from airflow import DAG

# BashOperator는 Airflow에서 가장 기본적인 Operator입니다.
# Operator는 DAG에서 실행할 작업을 정의합니다.
# 모든 Operator는 Airflow에서 작업을 실행하는 데 필요한 모든 인수를 포함하는 BaseOperator를 상속합니다.
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'owner-name',
    'depends_on_past': False,
    'email': ['your-email@g.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=15),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
with DAG(
    'tutorial',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 2, 1),
    catchup=False,
    tags=['example-sj'],
) as dag:
    
    # t1, t2, t3는 각각의 테스크이며 BashOperator를 사용합니다.
    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )
    
    t2 = BashOperator(
        task_id='sleep',
        depends_on_past=False,
        bash_command='sleep 5',
        retries=3,
    )
    
    t1.doc_md = dedent(
    """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
    """
    )

    dag.doc_md = __doc__  # DAG가 시작할 때 DocString을 보여주고 싶다면
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # 그렇지 않다면 아래와 같이 작성합니다.
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
    """
    )
    
    t3 = BashOperator(
        task_id='templated',
        depends_on_past=False,
        bash_command=templated_command,
        params={'my_param': 'Parameter I passed in'},
    )
    
    # 각 테스크를 연결합니다.
    t1 >> [t2, t3]
