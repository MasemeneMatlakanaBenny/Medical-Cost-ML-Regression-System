import joblib
import pandas as pd
from lib.configs import X_train_y_train,compute_model_metrics


test_df=pd.read_csv("data/test_data.csv")

## get the X_test and y_test:
X_test,y_test=X_train_y_train(test_df)

## load the relevant model -dt model:
dt_model=joblib.load("src/models/dt_reg_model.pkl")

## get the model metrics:
dt_metrics=compute_model_metrics(X_test=X_test,y_test=y_test,model=dt_model)

## save the metrics of the model:
joblib.dump(dt_metrics,"src/metrics/dt_metrics")


