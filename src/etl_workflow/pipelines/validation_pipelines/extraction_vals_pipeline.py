import pandas as pd
from great_expectations.core import Batch
from typing import List
from prefect import task,flow
from lib.validations import *
from lib.webhooks import send_discord_message


@task(
     name="get_extracted_data",
     description="The task for loading the extracted data",
     task_run_name="get_inital_data_task"
)
def load_extracted_data(df:pd.DataFrame)->pd.DataFrame:
    """
    Docstring for load_extracted_data
    
    :param df: Description
    :type df: pd.DataFrame
    :return: Description
    :rtype: DataFrame
    """

    df=pd.read_csv("data/extracted_df.csv")
    return df

## create the batch -> this will be used for validation later on:
@task(
    name="create_data_batch",
    description="Creating the data batch that will be used to test data quality checks",
    task_run_name="data_batch_task"
)
def create_data_batch(extracted_data:pd.DataFrame)->Batch:
    """
    Docstring for create_data_batch
    
    :param extracted_data: Description
    :type extracted_data: pd.DataFrame
    :return: Description
    :rtype: Any
    """
    batch=create_batch(df=extracted_data)

    return batch

##create data expectations:
@task(
    name="categorical_expectations",
    description="The data quality checks for categorical columns in the data",
    task_run_name="categorical_data_expectations"
)
def create_data_cat_expectations():
    """
    Docstring for create_data_expectations
    """
    gender_exp=create_categorical_expectations(column_name="gender",values=["Male","Female"])
    smoking_exp=create_categorical_expectations(column_name="smoker",values=["yes","no"])
    activity_exp=create_categorical_expectations(column_name="physical_activity_level",values=["Medium","High","Low"])
    city_exp=create_categorical_expectations(column_name="city_type",values=["Semi-Urban","Urban","Rural"])
    insurance_exp=create_categorical_expectations(column_name="insurance_type",values=["Private","Government","No Insurance"])

    exp_labels: List[str]=["gender_exp","smoking_exp","activity_exp","city_exp","insurance_exp"]
    data_exp: List[ExpectationConfiguration]=[gender_exp,smoking_exp,activity_exp,city_exp,insurance_exp]

    ## now return the expectations with corresponding labels:
    return data_exp,exp_labels


@task(
      name="diabetes_expectations",
      description="The data quality checks for the diabetes column in the data",
      task_run_name="diabetes_data_expectations"
)
def create_diabetes_expectations():

    # start first by creating the diabetes expectations:
    diabetes_min_exp=create_min_expectations(column_name="diabetes",min_value=0,max_value=0.01)
    diabetes_max_exp=create_max_expectations(column_name="diabtetes",min_value=1,max_value=1.1)
    diabetes_sum_exp=create_sum_expectations(column_name="diabetes",min_value=1000,max_value=10000)

    data_exp: List[ExpectationConfiguration]=[diabetes_min_exp,diabetes_max_exp,diabetes_sum_exp]
    exp_labels: List[str]=["diabetes_min","diabetes_max","diabetes_sum"]

    ## now return the expectations with corresponding labels:
    return data_exp,exp_labels


@task(
        name="age_expectations",
        description="The data quality checks for the age column",
        task_run_name="age_data_expectations"
)
def create_age_expectations():
    age_min_exp=create_min_expectations(column_name="age",min_value=18,max_value=19)
    age_max_exp=create_max_expectations(column_name="age",min_value=80,max_value=90)

    data_exp: List[ExpectationConfiguration]=[age_min_exp,age_max_exp]
    exp_labels:List[str]=["age_min","age_max"]

    ## now return the expectations with corresponding labels:
    return data_exp,exp_labels


@task(
        name="hyper_expectations",
        description="The data quality checks for hypertension",
        task_run_name="hypertension_data_expectations"
)
def create_hyper_expectations():
    ## create the hypertension expectations:
    hyper_min_exp=create_min_expectations(column_name="hypertension",min_value=0,max_value=0.1)
    hyper_max_exp=create_max_expectations(column_name="hypertension",min_value=1,max_value=1.1)
    hyper_sum_exp=create_sum_expectations(column_name="hypertension",min_value=1000,max_value=1500)

    data_exp: List[ExpectationConfiguration]=[hyper_min_exp,hyper_max_exp,hyper_sum_exp]
    exp_labels: List[str]=["hyper_min","hyper_max","hyper_sum"]

    ## now return the expectations with corresponding labels:
    return data_exp,exp_labels


@task(
    name="heart_expectations",
    description="The data quality checks for the heart disease",
    task_run_name="heart_data_expectations"
)
def create_heart_expectations():
    ## create the heart disease expectations:
    heart_min_exp=create_min_expectations(column_name="heart_disease",min_value=0,max_value=0.1)
    heart_max_exp=create_max_expectations(column_name="heart_disease",min_value=1,max_value=1.1)
    heart_sum_exp=create_sum_expectations(column_name="heart_disease",min_value=100,max_value=1500)

    data_exp:List[ExpectationConfiguration]=[heart_min_exp,heart_max_exp,heart_sum_exp]
    exp_labels: List[str]=["heart_min","heart_max","heart_sum"]

    ## now return the expectations with corresponding labels:
    return data_exp,exp_labels


@task(
    name="asthma_expectations",
    description="The data quality checks for asthma",
    task_run_name="asthma_data_expectations"
)
def create_asthma_expectations():
    ## create the asthma expectations:
    asthma_min_exp=create_min_expectations(column_name="asthma",min_value=0,max_value=0.1)
    asthma_max_exp=create_max_expectations(column_name="asthma",min_value=1,max_value=1.1)
    asthma_sum_exp=create_sum_expectations(column_name="asthma",min_value=100,max_value=1500)
    
    data_exp:List[ExpectationConfiguration]=[asthma_min_exp,asthma_max_exp,asthma_sum_exp]
    exp_labels: List[str]=["asthma_min","asthma_max","asthma_sum"]

    ## now return the expectations with corresponding labels:
    return data_exp,exp_labels


@task(
    name="data validations",
    description="Perform the data quality checks",
    task_run_name="data_validation"
)
def validate_data_expectations(batch:Batch,
                               expectations:List[ExpectationConfiguration]
                               ,expectation_labels:List[str]):
    """
    Docstring for validate_data_expectations
    
    :param expectations: Description
    :type expectations: List
    :param expectation_labels: Description
    :type expectation_labels: List
    """
    ## validate the data expectations:
    results_df=validate_expectations(batch=batch,expectations=expectations,expectation_labels=expectation_labels)

    return results_df


@task(
        name="save checks",
        description="Save the data quality checks for meta data validation",
        task_run_name="save_results_task"
)
def save_validation_results_df(path:str,df:pd.DataFrame):
    """
    Docstring for save_validation_results_df
    :param path: path to save the dataframe in a csv format
    :type path:str
    :param df: Description
    :type df: pd.DataFrame
    """
    df.to_csv(path)


@flow
def data_extraction_validation_workflow():
    
    ## load the extracted data first:
    extracted_df=load_extracted_data()

    ## create the data batch:
    batch=create_data_batch()

    ## create the data expectations along with corresponding labels
    cat_exp,cat_exp_labels=create_data_cat_expectations()

    ## validate the categorical data expectations:
    results_exp_cat=validate_data_expectations(batch=batch,
                                               expectations=cat_exp,
                                               expectation_labels=cat_exp_labels)
    
    ## save the categorical expectation results :
    save_validation_results_df(path="data_quality_checks/cat_results.csv",df=results_exp_cat)

    ## create the diabetes data expectations:
    diabetes_exp,diabetes_exp_labels=create_diabetes_expectations()

    ## validate the diabetes data expectations:
    results_exp_diabetes=validate_data_expectations(batch=batch,
                                                    expectations=diabetes_exp,
                                                    expectation_labels=diabetes_exp_labels)
    
    ## save the diabetes expectation results:
    save_validation_results_df(path="data_quality_checks/diabetes_results.csv",df=results_exp_diabetes)
    
    ## create the age data expectations:
    age_exp,age_exp_labels=create_age_expectations()


    ## validate the age data expectations:
    results_exp_age=validate_data_expectations(batch=batch,
                                               expectations=age_exp,
                                               expectation_labels=age_exp_labels)
    
    ## save the age data expectation results:
    save_validation_results_df(path="data_quality_checks/age_results.csv",df=results_exp_age)

     ## create the hyper data expectations:
    hyper_exp,hyper_exp_labels=create_hyper_expectations()

    ## validate the hyper data expectations:
    results_exp_hyper=validate_data_expectations(batch=batch,
                                                    expectations=hyper_exp,
                                                    expectation_labels=hyper_exp_labels)
    
    ## save the hyper data expectation results:
    save_validation_results_df(path="data_quality_checks/hyper_results.csv",df=results_exp_hyper)
    
    ## create the heart data expectations:
    heart_exp,heart_exp_labels=create_heart_expectations()

    ## validate the heart data expectations:
    results_exp_heart=validate_data_expectations(batch=batch,
                                               expectations=heart_exp,
                                               expectation_labels=heart_exp_labels)
    
    ## save the heart data expectation results:
    save_validation_results_df(path="data_quality_checks/heart_results.csv",df=results_exp_heart)
    
     ## create the heart data expectations:
    asthma_exp,asthma_exp_labels=create_asthma_expectations()

    ## validate the heart data expectations:
    results_asthma_exp=validate_data_expectations(batch=batch,
                                               expectations=asthma_exp,
                                               expectation_labels=asthma_exp_labels)
    
    ## save the asthma data expectation results:
    save_validation_results_df(path="data_quality_checks/asthma_results.csv",df=results_asthma_exp)


# run the data pipeline
if __name__=="__main__":
    data_extraction_validation_workflow()
