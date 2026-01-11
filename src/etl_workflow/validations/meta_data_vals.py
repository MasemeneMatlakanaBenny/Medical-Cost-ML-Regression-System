import pandas as pd
from typing import List
from great_expectations.core.batch import Batch
from great_expectations.expectations.expectation import ExpectationConfiguration

from lib.validations import create_batch,meta_validation

##get the data first:
validation_df=pd.read_csv("data_quality_checks/data_validation.csv")

## create the batch first:
meta_batch=create_batch(df=validation_df)

## validate the validations:
meta_vals=meta_validation(batch=meta_batch,column_name="results")

print(meta_vals[0])

