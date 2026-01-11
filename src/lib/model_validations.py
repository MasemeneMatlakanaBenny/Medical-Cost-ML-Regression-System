import pandas as pd
import great_expectations as gx
from great_expectations.expectations.expectation import ExpectationConfiguration
from typing import List,Union

def create_model_batch(df:pd.DataFrame):
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
    batch_definition=data_asset.add_batch_definition_whole_dataframe("model_batch")

    batch=batch_definition.get_batch(batch_parameters={"dataframe":df})

    return batch

def create_metric_expectation(metric_name:str,min_metric_score:Union[float,int],max_metric_score:Union[float,int]):
    """
    Docstring for create_min_accuracy_expectation
    
    :param column_name: the name of the column in the metrics dataset
    :type column_name: str
    :param min_metric_score: minimum expected metric score of the model
    :type min_metric_score: float
    :param max_metric_score: maximum expected metric score of the model
    :type max_metric_score: float
    """

    score_expectation=gx.expectations.ExpectColumnValuesToBeBetween(
        min_value=min_metric_score,max_value=max_metric_score,column=metric_name
    )

    return score_expectation


def validate_metric_expectations(batch,expectations:List[ExpectationConfiguration],labels:List[str]):
    """
    Docstring for validate_metric_expectations
    
    :param batch: Description
    :param expectations: Description
    :type expectations: List[ExpectationConfiguration]
    :param labels: Description
    :type labels: List[str]
    """

    expectation_results=[]

    for expectation in expectations:
        validation_exp=batch.validate(expectation)

        validation_results=validation_exp[0]

        expectation_results.append(validation_results)

    results_df=pd.DataFrame({
        "expectation":labels,
        "results":expectation_results
    })

    return results_df

