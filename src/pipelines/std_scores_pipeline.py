import pandas as pd
from prefect import task,flow
from lib.model_validations import create_model_batch,create_metric_expectation,validate_metric_expectations


## load the scores:
@task
def get_std_scores():
    """
    """
    std_scores=pd.read_csv("data/std_drift_scores.csv")
    
    return std_scores

## create the batch:
@task
def std_scores_validation(scores_df:pd.DataFrame):
    """
    """
    batch=create_model_batch(df=scores_df)
    ## create the expectation:
    exp=[create_metric_expectation(metric_name="drift_perc",min_metric_score=0.000,max_metric_score=0.1)]
    exp_labels=["std_score_exp"]
    
    ## get the results"
    validation_results=validate_metric_expectations(batch=batch,expectations=exp,labels=exp_labels)
    print(validation_results['results'])

@flow
def std_scores_workflow():
    """
    """

    scores_df=get_std_scores()

    std_scores_validation(scores_df=scores_df)


if __name__=="__main__":
    std_scores_workflow()
    
