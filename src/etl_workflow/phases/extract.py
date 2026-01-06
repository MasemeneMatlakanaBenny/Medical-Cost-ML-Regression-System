import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv


## load the .env file in the workflow first
load_dotenv()

##access the security codes /configurations:
password=os.getenv("PASSWORD")
user=os.getenv("USER")
schema_name=os.getenv("SCHEMA")
table_name=os.getenv("TABLE_NAME")

## create the engine first:
engine=create_engine(f"mysql+pymysql://{user}:{password}@127.0.0.1:3306/{schema_name}")

## create the query:
query=f"SELECT * FROM {table_name}"

## read the query using pandas 
df=pd.read_sql_query(query,engine)

## save the df as csv/parquet/xlsx file depending on the use case
df.to_csv("data/extracted_df.csv",index=False)


