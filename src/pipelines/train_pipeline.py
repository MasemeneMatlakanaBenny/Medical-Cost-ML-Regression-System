import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from prefect import task,flow
from lib.configs import X_train_y_train


@task
def linear_reg_model(X_train:pd.DataFrame,
                     y_train:pd.DataFrame)->LinearRegression:
    """
    """
    model=LinearRegression()

    model.fit(X_train,y_train)

    return model

@task
def dt_reg_model(
        X_train:pd.DataFrame,
        y_train:pd.DataFrame)-> DecisionTreeRegressor:
    """
    """
    model=DecisionTreeRegressor()

    model.fit(X_train,y_train)

    return model

@task
def save_model(model,model_path):
    """
    """
    joblib.dump(model,model_path)

@flow
def train_workflow():
    """
    """
    X_train,y_train=X_train_y_train()
    linear_model=linear_reg_model(X_train=X_train,y_train=y_train)
    dt_model=dt_reg_model(X_train=X_train,y_train=y_train)

    save_model(linear_model,model_path="src/models/linear_reg_model.pkl")
    save_model(dt_model,model_path="src/models/dt_reg_model.pkl")

if __name__=="__main__":
  train_workflow()
