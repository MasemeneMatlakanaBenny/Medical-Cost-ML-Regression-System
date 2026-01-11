import pandas as pd
import great_expectations as gx
import joblib
from typing import List
from great_expectations.expectations.expectation import ExpectationConfiguration
from lib.model_validations import create_model_batch,create_metric_expectations,validate_metric_expectations

## get the results_df:
results_df=pd.read_csv("model_quality_checks/reg_validations.csv")


## create the batch:
batch=create_model_batch(df=results_df)

## create the expectations:
expectation=gx.expectations.ExpectColumnDistinctValuesToEqualSet(
    value_set=["success"],column="results"
)

## expectations labels:
meta_validation=batch.validate(expectation)[0]

print(meta_validation)
