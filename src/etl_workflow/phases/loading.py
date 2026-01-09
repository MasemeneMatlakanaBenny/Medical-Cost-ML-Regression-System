
import pandas as pd
import hopsworks
import os
from dotenv import load_dotenv


load_dotenv()

## get the API_KEY and PROJECT_NAME from dotenv file:
api_key=os.getenv("API_KEY")
project_name=os.getenv("PROJECT_NAME")


## login hopsworks:
project=hopsworks.login(
    api_key_value=api_key,
    project=project_name
)

## create the feature store
feature_store=project.get_feature_store()

## create the feature view:
feature_name="medical_costs"
feature_version="1"

feature_description="features for medical cost ML system"

feature_view=feature_store.get_or_create_group(
    name=feature_name,
    version=feature_version,
    description=feature_description,
    primary_key=['userId'],
    event=['time_stamp']
)

