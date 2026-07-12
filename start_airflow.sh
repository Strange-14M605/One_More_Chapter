# set airflow home and dags folder
export AIRFLOW_HOME=$(pwd)/airflow
export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/dags

# launch airflow (not for production use, just for development and testing purposes)
airflow standalone