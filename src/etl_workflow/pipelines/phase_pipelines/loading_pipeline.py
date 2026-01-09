import pandas as pd
import hopsworks
from hopsworks.project import Project
from prefect import task,flow

## create the task for loading the data first:

@task
def load_transformed_data(path):
    """
    Docstring for load_transformed_data
    
    :param path: Path for the transformed dataset-> csv in this case
    """

    df=pd.read_csv(path)

    return df

@task
def create_project()->Project:
    """
    Docstring for load_credentials
    Load the API key value from .env folder and project name of hopsworks
    """
    import os
    from dotenv import load_dotenv

    load_dotenv()

    ## get the api key and project name:
    api_key=os.getenv("API_KEY")
    project_name=os.getenv("PROJECT_NAME")

    project=hopsworks.login(
        api_key_value=api_key,
        project=project_name
    )

    return project

@task
def create_feature_store(project:Project):
    """
    Docstring for create_feature_store
    
    :param project: the project created in hopsworks UI
    :type project: Project
    """

    feature_store=project.get_feature_store()

    return feature_store

@task
def create_feature_group(feature_store,name,description,primary_key,event):
    """
    Docstring for create_feature_group
    
    :param feature_store: Feature store that is used in the hopsworks
    :param name: Name of the feature group that will be used to store the dataset
    :param descripion: Description for the feature group
    :param primary_key: The primary key used to identify unique users
    :param event: The event time or datetime column available in the dataset
    """

    feature_group=feature_store.get_or_create_feature_group(
        name=name,
        description=description,
        primary_key=[primary_key],
        event=[event]
    )

    return feature_group


@flow
def data_loading_pipeline():
    """
    """

    ## load the transformed data:
    df=load_transformed_data(path="data/transformed_df.csv")

    ## create the hopsworks project:
    project=create_project()

    ## create the feature store:
    feature_store=create_feature_store(project=project)

    ## create the feature group:
    feature_group=create_feature_group(feature_store=feature_store,name="medical_df",description="Data for medical ML models",
                                       primary_key="userId",event="datetime")
    

## run the data_loading_pipeline
if __name__=="__main__":
    data_loading_pipeline()

    



