import pandas as pd
from lib.validations import *

## create the batch -> this will be used for validation later on:
df=pd.read_csv("data/transformed_df.csv")
batch=create_batch(df=df)

gender_exp=create_categorical_expectations(column_name="gender",values=["Male","Female"])

smoking_exp=create_categorical_expectations(column_name="smoker",values=["yes","no"])

activity_exp=create_categorical_expectations(column_name="physical_activity_level",values=["Medium","High","Low"])

city_exp=create_categorical_expectations(column_name="city_type",values=["Semi-Urban","Urban","Rural"])

insurance_exp=create_categorical_expectations(column_name="insurance_type",values=["Private","Government","No Insurance"])


## create numerical expectations:

## start first by creating the diabetes expectations:
diabetes_min_exp=create_min_expectations(column_name="diabetes",min_value=0,max_value=0.01)
diabetes_max_exp=create_max_expectations(column_name="diabtetes",min_value=1,max_value=1.1)
diabetes_sum_exp=create_sum_expectations(column_name="diabetes",min_value=1000,max_value=10000)

age_min_exp=create_min_expectations(column_name="age",min_value=18,max_value=19)
age_max_exp=create_max_expectations(column_name="age",min_value=80,max_value=90)

## create the hypertension expectations:
hyper_min_exp=create_min_expectations(column_name="hypertension",min_value=0,max_value=0.1)
hyper_max_exp=create_max_expectations(column_name="hypertension",min_value=1,max_value=1.1)
hyper_sum_exp=create_sum_expectations(column_name="hypertension",min_value=1000,max_value=1500)

## create the heart disease expectations:
heart_min_exp=create_min_expectations(column_name="heart_disease",min_value=0,max_value=0.1)
heart_max_exp=create_max_expectations(column_name="heart_disease",min_value=1,max_value=1.1)
heart_sum_exp=create_sum_expectations(column_name="heart_disease",min_value=100,max_value=1500)

## create the asthma expectations:
asthma_min_exp=create_min_expectations(column_name="asthma",min_value=0,max_value=0.1)
asthma_max_exp=create_max_expectations(column_name="asthma",min_value=1,max_value=1.1)
asthma_sum_exp=create_sum_expectations(column_name="asthma",min_value=100,max_value=1500)


expectations=[insurance_exp,diabetes_min_exp,diabetes_max_exp,diabetes_sum_exp,
              age_min_exp,age_max_exp,hyper_min_exp,hyper_max_exp,hyper_sum_exp,heart_min_exp,heart_max_exp,
              heart_sum_exp,asthma_min_exp,asthma_max_exp,asthma_sum_exp]

labels=["insurance_exp","diabetes_min","diabetes_max","diabetes_sum","age_min",
        "age_max","hyper_min","hyper_max","hyper_sum","heart_min","heart_max","heart_sum",
        "asthma_min","asthma_max","asthma_sum"]

results_expectations=validate_expectations(batch=batch,expectations=expectations,labels=labels)

## save df:
results_expectations.to_csv("data_quality_checks/data_validation.csv",index=False)

