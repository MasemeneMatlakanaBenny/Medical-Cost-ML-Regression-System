import joblib
import pandas as pd
from prefect import task,flow
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from typing import Union
from lib.configs import X_train_y_train,compute_model_metrics

@task(
        name="loading_data",
        task_run_name="load_test_data",
        description="Loading the test data that will be used to get the model metrics"
)
def load_test_data():
    """
    """
    test_df=pd.read_csv("data/test_data.csv")

    return test_df

## get the X_test and y_test:
@task(
        name="XY_Tests",
        task_run_name="X_test-y_test",
        description="Load the X_test and y_test"
)
def X_test_y_test(test_df:pd.DataFrame):
    """
    """
    X_test,y_test=X_train_y_train(test_df)

    return X_test,y_test
## load the relevant model -dt model:
@task(
        name="model_loading",
        task_run_name="get_model",
        description="Get the model and make it available for metrics computation"
)
def load_model(path:str):
    """
    """
    model=joblib.load(path)
    return model

 ## get the model metrics:
@task(
        name="computation",
        task_run_name="metrics_computation",
        description="Computing the model metrics"
)
def model_metrics(X_test,y_test,model:Union[LinearRegression,DecisionTreeRegressor]):
    """
    """
    ## get the model metrics:
    metrics=compute_model_metrics(X_test=X_test,y_test=y_test,model=model)

    return metrics

 ## save the metrics of the model:
@task(
        name="save_metrics",
        description="Save the model metrics",
        task_run_name="metrics_saving"
)
def save_metrics(metrics,path):
    """
    """
    joblib.dump(metrics,path)

@flow
def evaluation_workflow():
    
    ## test dataframe:
    test_df=load_test_data()

    ## get X_test and y_test:
    X_test,y_test=X_test_y_test(test_df=test_df)

    ## load the model:
    reg_model=load_model(path="src/models/linear_reg_model.pkl")

    dt_model=load_model(path="src/models/dt_reg_model.pkl")

    ## get the metrics:
    reg_metrics=model_metrics(X_test=X_test,y_test=y_test,model=reg_model)

    dt_metrics=model_metrics(X_test=X_test,y_test=y_test,model=dt_model)

    ## save the metrics:
    save_metrics(reg_metrics,"src/metrics/linear_reg_model_metrics.pkl")

    save_metrics(dt_metrics,"src/metrics/dt_reg_model_metrics.pkl")

if __name__=="__main__":
    evaluation_workflow()
