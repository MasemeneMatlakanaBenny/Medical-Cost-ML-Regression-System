## make predictions on test data:
import joblib
import pandas as pd
from lib.configs import X_train_y_train,compute_model_metrics


test_df=pd.read_csv("data/test_data.csv")

## get the X_test and y_test:
X_test,y_test=X_train_y_train(test_df)

## get the model:
model=joblib.load("src/models/linear_reg_model.pkl")


## get the predictions:
predictions=model.predict(X_test)

## save as df:
pred_df=pd.DataFrame({"predictions":predictions})
## save the predictions:
pred_df.to_csv("data/predictions.csv",index=False)
