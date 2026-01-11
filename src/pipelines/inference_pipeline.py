import pandas as pd
import joblib
from prefect import task,flow

@task
def get_infer_data(path):
    """
    """
    df=pd.read_csv(path)

    return df

@task
def linear_model_pred(infer_data:pd.DataFrame):
    """
    Docstring for linear_model_pred
    
    :param infer_data: new data to predict on
    :type infer_data: pd.DataFrame
    """

    model=joblib.load("src/models/linear_reg_model.pkl")
    X_df=infer_data.drop("annual_medical_cost")


    predictions=model.predict(X_df)

    return predictions

@flow
def inference_workflow(df_path:str):
    """
    """
    infer_df=get_infer_data(path=df_path)

    predictions=linear_model_pred(infer_data=infer_df)

    return predictions

