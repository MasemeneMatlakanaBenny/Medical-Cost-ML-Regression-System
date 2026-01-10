import pandas as pd
from sklearn.model_selection import train_test_split

df=pd.read_csv("data/loaded_df.csv")


num_data=df.select_dtypes(include='number')

train_df,test_df=train_test_split(num_data,test_size=0.2,random_state=42)


## save both the train and test sets to the data file:
train_df.to_csv("data/train_data.csv",index=False)
test_df.to_csv("data/test_data.csv",index=False)
