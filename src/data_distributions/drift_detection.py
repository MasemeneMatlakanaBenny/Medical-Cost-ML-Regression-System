import numpy as np
import pandas as pd

np.Inf=np.inf
np.NINF=np.inf

from deepchecks.tabular.dataset import Dataset
from deepchecks.tabular.checks import FeatureDrift
from lib.configs import X_train_y_train

X_train,y_train=X_train_y_train()

train_df=pd.read_csv("data/train_df.csv")

test_df=pd.read_csv("data/test_df.csv")

train_checks=Dataset(train_df,cat_features=[])
test_checks=Dataset(test_df,cat_features=[])


drift=FeatureDrift()

results=drift.run(train_dataset=train_checks,test_dataset=test_checks)

features=X_train.columns
drift_scores=[]

for feature in features:
    drift_score=results[feature]['Drift score']

    drift_scores.append(drift_score)

drift_df=pd.DataFrame(
    {"features":feature,
     "drift_score":drift_scores}
)


drift_df.to_csv("data/drift_scores.csv")

