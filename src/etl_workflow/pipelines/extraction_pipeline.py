import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from prefect import task,flow

load_dotenv()

@task
def create_engine_connection():
    """
    """
    ##access the security codes /configurations:

    password=os.getenv("PASSWORD")
    user=os.getenv("USER")
    schema_name=os.getenv("SCHEMA")

    ## create the engine first:
    engine=create_engine(f"mysql+pymysql://{user}:{password}@127.0.0.1:3306/{schema_name}")

    return engine

@task
def data_extraction(engine):
    """
    Docstring for data_extraction
    
    :param engine: Description
    :param query: Description
    :type query: str
    """
    ## create the query:
    table_name=os.getenv("TABLE_NAME")
    query=f"SELECT * FROM {table_name}"

    ## read the query using pandas 
    df=pd.read_sql_query(query,engine)

    ## save the df as csv/parquet/xlsx file depending on the use case
    df.to_csv("data/extracted_df.csv",index=False)


@flow
def data_extraction_pipeline():
    """
    Docstring for data_extraction_pipeline
    Connect to the database via an Engine->
    Query the tables stored in the schema->
    Boom data extracted

    """
    engine=create_engine_connection()

    data_extraction(engine=engine)

if __name__=="__main__":
    data_extraction_pipeline()
    
