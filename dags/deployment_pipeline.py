# DEPLOYMENT PIPELINE
# frequency: when a new model is approved

# 1. define latest model in airflow config
# 2. load into service layer i.e. deploy model

# Output: 
# changes to app config under src/app/

# possible future work:
# Caching strategies
# Docker images and rollback/smoke tests

from pathlib import Path
from airflow.sdk import dag, task, get_current_context

@dag(
    dag_id="deployment_pipeline",
    schedule=None,
    catchup=False,
)
def deployment_pipeline():
    @task
    def pull_latest_model():
        context = get_current_context()
        model = context["dag_run"].conf.get("model", "popularity/v1")
        config_path = Path(__file__).resolve().parents[1] / "src" / "deployment" / "config.py"
        config_path.write_text(
            f'MODEL_PATH = "artifacts/models/{model}/recommendations.parquet"\n',
            encoding="utf-8",
        )

    pull_latest_model()


deployment_pipeline()