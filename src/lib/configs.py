import pandas as pd
from sklearn.metrics import root_mean_squared_error,mean_squared_error,r2_score

def X_train_y_train(train_df:pd.DataFrame):
    """
    Docstring for X_train_y_train
    
    :param train_df: train dataframe
    :type train_df: pd.DataFrame
    """
    label="annual_medical_cost"
    X_train=train_df.drop(label,axis=1)
    y_train=train_df[label]

    return X_train_y_train

def compute_model_metrics(X_test,y_test,model):
    """
    Docstring for compute_model_metrics
    
    :param X_test: X_test dataframe
    :param y_test: y_test dataframe
    """

    ## get the model's predictions first:
    y_preds=model.predict(X_test)

    ## get the key metrics now:
    mse_model=mean_squared_error(y_test,y_preds)
    rmse_model=root_mean_squared_error(y_test,y_preds)
    r2_model=r2_score(y_test,y_preds)

    ## combine the metrics with the use of the dictionary:
    metrics={
        "MSE":mse_model,
        "RMSE":rmse_model,
        "R-squared":r2_model
    }

    return metrics

