import pandas as pd
from lib.model_validations import create_model_batch,create_metric_expectation,validate_metric_expectations

## load the scores:
std_scores=pd.read_csv("data/std_drift_scores.csv")

## create the batch:
batch=create_model_batch(df=std_scores)

## create the expectation:
exp=[create_metric_expectation(metric_name="drift_perc",min_metric_score=0.000,max_metric_score=0.1)]

exp_labels=["std_score_exp"]

## get the results"
validation_results=validate_metric_expectations(batch=batch,expectations=exp,labels=exp_labels)

print(validation_results['results'])
