import pandas as pd
import numpy as np
from datetime import datetime
from prefect import task,flow

@task
def load_extracted_data(path:str):
    """
    Docstring for load_extracted_data
    
    :param path: Description
    """

    df=pd.read_csv(path)

    return df

@task
def fill_nulls(df:pd.DataFrame)->pd.DataFrame:
    """
    Docstring for fill_nulls
    
    :param df: Description
    :type df: pd.DataFrame
    :return: Description
    :rtype: DataFrame
    """
    
    ## if no insurance -> fill with nulls
    df["insurance_type"]=df["insurance_type"].fillna("No Insurance")

    return df

@task
def add_event_time_unique_id(df:pd.DataFrame)->pd.DataFrame:
    """
    Docstring for add_event_time_unique_id
    
    :param df: Description
    :type df: pd.DataFrame
    :return: Description
    :rtype: DataFrame
    """
    df["userId"]=np.arange(1,len(df)+1)
    df["time_event"]=datetime.now()
    ## save the df now:
    df.to_csv("transformed_df.csv",index=False)

    return df

@flow
def data_transformation_pipeline():

    ## load the extracted data:
    extracted_df=load_extracted_data(path="data/extracted_df.csv")

    filled_nulls_df=fill_nulls(df=extracted_df) 

    transformed_df=add_event_time_unique_id(df=filled_nulls_df)

    return transformed_df

if __name__=="__main__":
    data_transformation_pipeline()

