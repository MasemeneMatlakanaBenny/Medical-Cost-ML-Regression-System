## here we transform the dataset and select the most relevant one that will be crucial ahead of the entire ML Workflow
import pandas as pd
import numpy as np
from datetime import datetime

##load the extracted df:
df=pd.read_csv("data/extracted_df.csv")

df["userId"]=np.arange(1,len(df)+1)
df["time_event"]=datetime.now()


## if no insurance -> fill with nulls
df["insurance_type"]=df["insurance_type"].fillna("No Insurance")

print(df.info()) ## to check if there are any nulls remaining or not

## save the df now:
df.to_csv("data/transformed_df.csv",index=False)
