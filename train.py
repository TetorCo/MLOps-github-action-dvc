import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import ADASYN
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score

def eval_metircs(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

df = pd.read_csv('dvc_players_stats.csv', index_col=0)
train, test = train_test_split(df, test_size=0.2, random_state=7)
target = 'PFA_Team'


X_train = train.drop([target], axis=1)
y_train = train[target]
X_test = test.drop([target], axis=1)
y_test = test[target]


ads = ADASYN(random_state=7, n_neighbors=5)  # 데이터 불균형 때문에 ADASYN 사용
X_train_ads, y_train_ads = ads.fit_resample(X_train, y_train)
model = RandomForestClassifier(n_estimators=100, max_depth=50, random_state=7)
model.fit(X_train_ads, y_train_ads)


train_score = model.score(X_train, y_train) * 100
test_score = model.score(X_test, y_test) * 100

predict_model = model.predict(X_test)
(rmse, mae, r2) = eval_metircs(y_test, predict_model)

with open("metrics.json", 'w') as outfile:
        json.dump({"RMSE": rmse, "MAE": mae, "R2":r2}, outfile)


importances = model.feature_importances_
labels = df.columns
feature_df = pd.DataFrame(list(zip(labels, importances)), columns = ["feature","importance"])
feature_df = feature_df.sort_values(by='importance', ascending=False,)


# image formatting
axis_fs = 18 #fontsize
title_fs = 22 #fontsize
sns.set(style="whitegrid")

ax = sns.barplot(x="importance", y="feature", data=feature_df)
ax.set_xlabel('Importance',fontsize = axis_fs)
ax.set_ylabel('Feature', fontsize = axis_fs)
ax.set_title('Random forest\nfeature importance', fontsize = title_fs)

plt.tight_layout()
plt.savefig("feature_importance.png",dpi=120)
plt.close()