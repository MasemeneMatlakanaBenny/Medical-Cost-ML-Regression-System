import mlflow
from lib.mlflow_configs import create_experiment,set_mlflow_host,load_project_tags

set_mlflow_host()

create_experiment(
  experiment_name="medical_cost_exp",
  tags=load_project_tags()
)
