import joblib
import pandas as pd
from lib.configs import X_train_y_train,compute_model_metrics


test_df=pd.read_csv("data/test_data.csv")

## get the X_test and y_test:
X_test,y_test=X_train_y_train(test_df)

## load the relevant model -linear model:
linear_model=joblib.load("src/models/linear_reg_model.pkl")

## get the model metrics:
dt_metrics=compute_model_metrics(X_test=X_test,y_test=y_test,model=linear_model)

## save the metrics of the model:
joblib.dump(dt_metrics,"src/metrics/linear_reg_metrics")

