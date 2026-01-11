import mlflow
from mlflow.models import infer_signature
from lib.configs import X_train_y_train
from lib.mlflow_configs import set_mlflow_host,set_mlflow_running_experiment,mlflow_client
from lib.mlflow_configs import load_model_info


## set the mlflow host and running/active experiment within the mlflow host:
set_mlflow_host()

set_mlflow_running_experiment(experiment_name="medical_cost_exp")
## get the X_train and y_train:
X_train,y_train=X_train_y_train()

signature=infer_signature(X_train,y_train)
model_name,model=load_model_info(model_name="dt_model",model_path="src/models/dt_reg_model.pkl")

with mlflow.start_run(run_name="dt_run") as run:
    
    ## register the model on mlflow local host:
    mlflow.sklearn.log_model(
        sk_model=model,
        signature=signature,
        registered_model_name=model_name
        )
