# import libs first:
import mlflow
from mlflow.client import MlflowClient
from mlflow.models import infer_signature

## declare some important variables that will be required in the process:

host="https://127.0.0.1:5000"

## define the experiment name and details:
exp_name="Medical Cost Experiement"

exp_description="Predicting the medical cost of the clients"

## the tags:
project_tags={
    "project_name":"Medical Cost Regression Project",
    "date":"2025 Dec - Jan 2026",
    "owner":"Mat Benny",
    "mlflow.note.experiment":exp_description
}


## create the experiment function:
def create_experiment(experiment_name:str,tags):
    """
    Docstring for create_experiment
    
    :param experiment_name: The name of the experiment
    :param tags: The tags for the experiment
    :type experiment_name: str
    """
    experiment=mlflow.create_experiment(
        name=experiment_name,
        tags=project_tags
    )

    return experiment

## the function for loading the host:
def load_mlflow_host():
    return host

## the function for loading the experiment name:
def load_running_experiment(experiment_name:str=exp_name):
    """
    Docstring for load_running_experiment
    
    :param experiment_name: The name of the experiment
    :type experiment_name: str
    """
    return experiment_name

## the function for setting the local host within the mlflow server:
def set_mlflow_host(host=host):
    """
    Docstring for set_mlflow_host
    
    :param host: where mlflow is running
    """

    return mlflow.set_tracking_uri(uri=host)

## the function for setting the experiment within the mlflow server:
def set_mlflow_running_experiment(experiment_name:str=exp_name):
    """
    Docstring for set_mlflow_running_experiment
    
    :param experiment_name: The name of the experiment
    :type experiment_name: str
    """

    return mlflow.set_experiment(experiment_name=experiment_name)

## the function for returning the MlflowClient:
def mlflow_client(host=host):
  
  client=MlflowClient(tracking_uri=host)
  
  return client

## the function for loading the model name:
def load_model_info(model_name:str,model_path:str):
    """
    Docstring for load_model_info
    
    :param model_name: Name of the model
    :type model_name: str
    :param model_path: Path of the model- joblib or json file 
    :type model_path: str
    """
    return model_name,model_path

## function for testing model registry
def test_model_registry(name, version,client_var=mlflow_client()):
    from mlflow.exceptions import RestException
    """
    Check if a specific model version exists in MLflow Model Registry
    and print the result.

    Args:
        name (str): Model name in the registry.
        version (str or int): Version number of the model.
    """
    client = client_var
    try:
        client.get_model_version(name=name, version=version)
        print(f"Model {name} version {version} exists")
    except RestException:
        print(f" Model {name} version {version} not found")
        

## a function for testing model versioning or stages per model
def test_model_versioning(name, stage,client_var=mlflow_client()):

    from mlflow.exceptions import RestException
    """
    Check if a specific model version exists in MLflow Model Registry
    and print the result.

    Args:
        name (str): Model name in the registry.
        version (str or int): Version number of the model.
    """
    client = mlflow_client()
    try:
        client.get_model_version(name=name, stage=stage)
        print(f"Model {name} at {stage} exists")
    except RestException:
        print(f"Model {name} at {stage} not found")
