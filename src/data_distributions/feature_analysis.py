import pandas as pd
from lib.feature_selection import detect_variation_drift


## load the train and test sets:
train_df=pd.read_csv("data/train_data.csv")

test_df=pd.read_csv("data/test_data.csv")

##get the std scores:
std_scores=detect_variation_drift(train_df=train_df,test_df=test_df)

## save the std scores in a csv format file:
std_scores.to_csv("data/std_drift_scores.csv",index=False)
