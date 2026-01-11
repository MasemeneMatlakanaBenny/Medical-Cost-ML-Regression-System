
import numpy as np
import pandas as pd
from typing import List
from prefect import task,flow

np.Inf=np.inf
np.NINF=np.inf

from deepchecks.tabular.dataset import Dataset
from deepchecks.tabular.checks import FeatureDrift
from lib.configs import X_train_y_train

## load the train/test/val file
@task
def load_df_file(path:str)->pd.DataFrame:
    """
    Docstring for load_df_file
    
    :param path: Description
    :type path: str
    :return: Description
    :rtype: DataFrame
    """

    df=pd.read_csv(load_df_file)

    return df


## create the checks dataset which can be used in the drift suites
@task
def tabular_checks_data(df:pd.DataFrame,cat_features:List[str]=None)->Dataset:
    """
    Docstring for tabular_checks_data
    
    :param df: Description
    :type df: pd.DataFrame
    :param cat_features: Description
    :type cat_features: List[str]
    """
    checks_data=Dataset(df=df,cat_features=cat_features)
    return checks_data

## get the drift results
@task
def drift_results(train_data:Dataset,test_data:Dataset):
    """
    """
    
    drift=FeatureDrift()

    results=drift.run(train_dataset=train_data,test_dataset=test_data)

    return results

## get the drift scores in a pandas dataframe
@task
def drift_scores_df(drift_results,features:List[str])->pd.DataFrame:
    """
    """
   
    drift_scores=[]
    for feature in features:
        drift_score=drift_results[feature]['Drift score']
        
        drift_scores.append(drift_score)
        
        drift_df=pd.DataFrame(
    {"features":feature,
     "drift_score":drift_scores}
        )

        return drift_df

## run the entire workflow with a simple pipeline
@flow
def drift_detection_workflow():

   ## get the X_train and y_traij
    X_train,y_train=X_train_y_train()
  
    ## get the train and test sets
    train_df=load_df_file("data/train_df.csv")
    
    test_df=load_df_file("data/test_df.csv")

  ## create deepchecks dataset for both train and test sets
    train_checks=tabular_checks_data(train_df,cat_features=None)
    test_checks=tabular_checks_data(test_df,cat_features=None)
  
  ## get the results 
    results=drift_results()

  ## get scores
    drift_df=drift_scores_df(drift_results=results,features=X_train.columns)

  ## save the pandas dataframe in a csv format
    drift_df.to_csv("data/drift_scores.csv")

if __name__=="__main__":
    drift_detection_workflow()

