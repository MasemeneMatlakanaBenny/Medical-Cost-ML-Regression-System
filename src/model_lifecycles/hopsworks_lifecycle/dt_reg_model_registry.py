import pandas as pd
import os
import hopsworks
from dotenv import load_dotenv
from hsml.schema import Schema
from hsml.model_schema import ModelSchema
from lib.configs import X_train_y_train

## load the .env folder 
load_dotenv()

## get the project name and api key first:
project_name=os.getenv("PROJECT_NAME")
api_key=os.getenv("API_KEY")


## get the project:
project=hopsworks.login(
    project=project_name,
    api_key_value=api_key
)

## load the train set
train_df=pd.read_csv("data/transformed_df.csv")

## get the X_train and ty_train
X_train,y_train=X_train_y_train(train_df=train_df)

## define both the input schema and output schema
input_schema=Schema(X_train)
output_schema=Schema(y_train)

## define the model schema ->more or less what is expected when serving the model in the future
model_schema=ModelSchema(input_schema=input_schema,output_schema=output_schema)


## model registry using the project created in hospworks:
model_registry=project.get_model_registry()


model=model_registry.sklearn.create_model(
    name="dt_model",
    model_schema=model_schema
)
)
