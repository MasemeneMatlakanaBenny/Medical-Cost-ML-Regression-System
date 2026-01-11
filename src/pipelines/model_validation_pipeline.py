import pandas as pd
import joblib
import great_expectations as gx
from typing import List
from prefect import task,flow
from great_expectations.expectations.expectation import ExpectationConfiguration
from great_expectations.core.batch import Batch
from lib.model_validations import create_model_batch,create_metric_expectations,validate_metric_expectations

## get the model metrics first:
@task
def create_metrics_df(metrics_path:str)->pd.DataFrame:
    """
    Docstring for create_metrics_df
    
    :param metrics_path: Description
    :type metrics_path: str
    :return: Description
    :rtype: DataFrame
    """
    metrics=joblib.load(metrics_path)

    ## convert the metrics into a df:
    metrics_df=pd.DataFrame([metrics])

    return metrics_df

## create the model validation 
@task
def model_validation_results(metrics_df:pd.DataFrame)->pd.DataFrame:
    """
    Docstring for model_validation_results
    
    :param model_metrics: Description
    :type model_metrics: pd.DataFrame
    :return: Description
    :rtype: DataFrame
    """
    
    batch:Batch=create_model_batch(df=metrics_df)
    
    ## create the expectations:
    r_squared_exp=create_metric_expectations(metric_name='R-squared',min_metric_score=0.8,max_metric_score=0.95)
    rmse_exp=create_metric_expectations(metric_name='mse',min_metric_score=0,max_metric_score=2200)

    ## expectations labels & expectations:
    exp_labels:List[str]=["r_squared_exp","rmse_exp"]

    expectations:List[ExpectationConfiguration]=[r_squared_exp,rmse_exp]

    ## validate the expectations:
    results_df=validate_metric_expectations(batch=batch,expectations=expectations,labels=exp_labels)

    return results_df

@task
def meta_model_validation(batch:Batch,validation_results:pd.DataFrame)->str:
    """
    Docstring for meta_model_validation
    
    :param validation_results: Description
    :type validation_results: pd.DataFrame
    :return: Description
    :rtype: str
    """
    ## create the expectations:
    expectation=gx.expectations.ExpectColumnDistinctValuesToEqualSet(
    value_set=["success"],column="results")

    ## expectations labels:
    meta_validation=batch.validate(expectation)

    meta_results=meta_validation[0]

    return meta_results

@flow
def model_validation_workflow():
    """
    Docstring for model_validation_workflow
    """

    ## get both decision tree model metrics and linear model metrics:

    ###this is now a dataframe storing decision tree model metrics
    dt_metrics_df=create_metrics_df(metrics_path="src/metrics/dt_metrics.pkl") 

    ### this is now a dataframe storing linear regression model metrics
    linear_metrics_df=create_metrics_df(metrics_path="src/metrics/linear_reg_metrics.pkl") ## this is now a dataframe

    ## get the validation results where we store the expectation and the validated results for each model:
    dt_validation_results_df=model_validation_results(metrics_df=dt_metrics_df)
    linear_validation_results_df=model_validation_results(metrics_df=dt_metrics_df)

    ### perform meta validation for each validated results:
    meta_dt_batch=create_model_batch(df=dt_validation_results_df)
    meta_dt_validation=meta_model_validation(batch=meta_dt_batch,validation_results=dt_validation_results_df)

    meta_linear_batch=create_model_batch(df=linear_validation_results_df)
    meta_linear_validation=meta_model_validation(batch=meta_linear_batch,validation_results=linear_validation_results_df)

    ## get the meta results:
    print(f"Meta Validation For Decision Tree Model:{meta_dt_validation}")
    print(f"Meta Validation For Regression Model:{meta_linear_validation}")

if __name__=="__main__":
    model_validation_workflow()
