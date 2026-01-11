import pandas as pd
import great_expectations as gx
from great_expectations.expectations.expectation import ExpectationConfiguration
from great_expectations.core.batch import Batch
from typing import List,Union

def create_batch(df:pd.DataFrame)->Batch:
    """
    Docstring for create_batch
    
    :param df: Dataset 
    :type df: pd.DataFrame

    """
    ## create the context first:
    context=gx.get_context()

    ## create the data source:
    data_source=context.data_sources.add_pandas("pandas")

    ## create the data asset:
    data_asset=data_source.add_dataframe_asset("data_asset")

    ## create the batch:
    batch_definition=data_asset.add_batch_definition_whole_dataframe("batch")

    batch=batch_definition.get_batch(batch_parameters={"dataframe":df})

    return batch

def create_categorical_expectations(column_name:str,
                                    values=List[str])->ExpectationConfiguration:
    
    """
    Docstring for create_categorical_expectations
    
    :param column_name: name of the column
    :type column_name: str
    :param values: distinct values in the column
    """
    expectations=gx.expectations.ExpectColumnDistinctValuesToContainSet(
        column=column_name,value_set=values
    )

    return expectations

def create_min_expectations(column_name:str,
                            min_value:Union[int,float],
                            max_value:Union[int,float])->ExpectationConfiguration:
    """
    Docstring for create_min_expectations
    
    :param column_name: name of the column
    :type column_name: str
    :param min_value: minimum value expected
    :param max_value: maximum value expected
    """

    expectations=gx.expectations.ExpectColumnMinToBeBetween(
        column=column_name,min_value=min_value,max_value=max_value
    )

    return expectations

def create_sum_expectations(column_name:str,
                            min_value:Union[int,float],
                            max_value:Union[int,float])->ExpectationConfiguration:
    """
    Docstring for create_sum_expectations
    
    :param column_name: Description
    :type column_name: str
    :param min_value: miminum value expected
    :type min_value: Union[int, float]
    :param max_value: Description
    :type max_value: Union[int, float]
    """
    expectations=gx.expectations.ExpectColumnSumToBeBetween(
        column=column_name,min_value=min_value,max_value=max_value
    )

    return expectations
def create_max_expectations(column_name:str,
                            min_value:Union[int,float],
                            max_value:Union[int,float])->ExpectationConfiguration:
    """
    Docstring for create_max_expectations
    :param column_name: Description
    :type column_name: str
    :param min_value: Description
    :type min_value: Union[int, float]
    :param max_value: Description
    :type max_value: Union[int, float]
    """
    expectations=gx.expectations.ExpectColumnMaxToBeBetween(
        column=column_name,min_value=min_value,max_value=max_value
    )

    return expectations


def create_mean_expectations(column_name:str,
                             min_value:Union[int,float],
                             max_value:Union[int,float])->ExpectationConfiguration:

    """
    Docstring for create_mean_expectations
    
    :param column_name: Description
    :type column_name: str
    :param min_value: Description
    :type min_value: Union[int, float]
    :param max_value: Description
    :type max_value: Union[int, float]
    """

    expectations=gx.expectations.ExpectColumnMeanToBeBetween(
        column=column_name,min_value=min_value,max_value=max_value
    )

    return expectations

def validate_expectations(batch:Batch,
                          expectations:List[ExpectationConfiguration]
                          ,labels:List[str])->pd.DataFrame:
    """
    """

    validation_results=[]
    for expectation in expectations:
        results=batch.validate(expectation)

        validation_results.append(results[0])

    results_df=pd.DataFrame({"label":labels,"results":validation_results})

    return results_df

def meta_validation(batch:Batch,column_name:str):
    """
    """

    expectation=gx.expectations.ExpectColumnDistinctValuesToEqualSet(
        value_set=["success"],column=column_name
    )

    results=batch.validate(expectation)[0]

    return results


def load_quality_checks_results(path)->pd.DataFrame:
    """
    """

    df=pd.read_csv(path)

    return df
