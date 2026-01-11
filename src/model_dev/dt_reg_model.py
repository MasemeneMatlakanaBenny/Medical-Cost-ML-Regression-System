import joblib
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from lib.configs import X_train_y_train

train_df=pd.read_csv("data/train_data.csv")


## load the X_train and y_train
X_train,y_train=X_train_y_train(train_df=train_df)

## fit the model:
model=DecisionTreeRegressor()

model.fit(X_train,y_train)

## save the model with joblib
joblib.dump(model,"src/models/dt_reg_model.pkl")
