import mlflow
import mlflow.sklearn
from lib.mlflow_configs import set_mlflow_host,set_mlflow_running_experiment,mlflow_client


## set the mlflow host and experiment within the mlflow server:
set_mlflow_host()
set_mlflow_running_experiment()

## create the client -> will be used to move the model from the registry to staging phase
client=mlflow_client()

model_name="dt_model"
model_version=1

## productionize the model:
client.transition_model_version_stage(
    name=model_name,
    version=model_version,
    stage="production"
)

