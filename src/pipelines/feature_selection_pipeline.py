import pandas as pd
from prefect import task,flow
from lib.feature_selection import detect_variation_drift


## load the train and test sets:
@task 
def detect_std_drift():
    """
    """
    train_df=pd.read_csv("data/train_data.csv")
    test_df=pd.read_csv("data/test_data.csv")
    ##get the std scores:

    std_scores=detect_variation_drift(train_df=train_df,test_df=test_df)
    
    return std_scores

## save the std scores in a csv format file:
@task
def save_std_scores(std_scores):
    """
    """
    std_scores.to_csv("data/std_drift_scores.csv",index=False)

@flow
def feature_selection_workflow():

    ## get the std scores:
    std_scores=detect_std_drift()

    ## save std scores:
    save_std_scores(std_scores=std_scores)

if __name__=="__main__":
    feature_selection_workflow()

