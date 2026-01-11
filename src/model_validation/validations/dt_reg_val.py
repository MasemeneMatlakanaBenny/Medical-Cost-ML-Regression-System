import pandas as pd
import joblib
from typing import List
from great_expectations.expectations.expectation import ExpectationConfiguration
from lib.model_validations import create_model_batch,create_metric_expectation,validate_metric_expectations

## get the model metrics first:
metrics=joblib.load("src/metrics/dt_metrics.pkl")

## convert the metrics into a df:
metrics_df=pd.DataFrame([metrics])

## create the batch:
batch=create_model_batch(df=metrics_df)

## create the expectations:
r_squared_exp=create_metric_expectation(metric_name='R-squared',min_metric_score=0.8,max_metric_score=0.95)
rmse_exp=create_metric_expectation(metric_name='mse',min_metric_score=0,max_metric_score=2200)

## expectations labels:
exp_labels:List[str]=["r_squared_exp","rmse_exp"]

## create the expectations:
expectations:List[ExpectationConfiguration]=[r_squared_exp,rmse_exp]

## validate the expectations:
results_df=validate_metric_expectations(batch=batch,expectations=expectations,labels=exp_labels)

results_df.to_csv("model_quality_checks/dt_validations.csv",index=False)


