import pandas as pd
import pickle
import psycopg2
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import ADASYN
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score
from sklearn.preprocessing import Binarizer
### over_sampling 진행 한 후 비교를 위해 추가
from collections import Counter

conn = psycopg2.connect(
    host="arjuna.db.elephantsql.com",
    database="oigajbtw",
    user="oigajbtw",
    password="z0zOhSY5EZA5JROgmkuF2C5_dXt0IQ4S")
cur = conn.cursor()

cur.execute("SELECT * FROM player_mf")
mf_table = cur.fetchall()
mf_df = pd.DataFrame(mf_table, columns=[x[0] for x in cur.description])

# text columns 변환
mf_df['Passes'] = mf_df['Passes'].str.replace(',', '').astype('int64')

### 머신러닝 모델 만들기
"""
순서
1. 데이터는 이미 있음
2. train, test set 나눠서 학습 target = 'PFA_Team'
2-1. 불균형한 데이터이므로 oversapling 진행
3. 모델 조정
columns = ['Appearances', 'Goals', 'Assists', 'Big chances created']
"""
train, test = train_test_split(mf_df, test_size=0.2, random_state=7)
train, val = train_test_split(train, test_size=0.2, random_state=7)

target = 'PFA_Team'
features = ['Appearances', 'Goals', 'Assists', 'Big chances created']

X_train = train[features]
y_train = train[target]
X_val = val[features]
y_val = val[target]
X_test = test[features]
y_test = test[target]


# 랜덤포레스트 및 ADASYN OverSampling
# print(y_counter) # Counter({0: 785, 1: 8}) 상당히 불균형한 데이터 -> over_sampling 진행
ads = ADASYN(random_state=7, n_neighbors=5)
X_train_ads, y_train_ads = ads.fit_resample(X_train, y_train)
# print(Counter(y_train_ads)) # Counter({0: 785, 1:785}) 데이터 내부에서 균형을 맞췄다.


model = RandomForestClassifier(n_estimators=100, random_state=7)
model.fit(X_train_ads, y_train_ads)


# model pickle에 저장
with open('model_mf.pkl', 'wb') as pickle_file:
    pickle.dump(model, pickle_file)

if __name__ == "__main__":
    def get_score(y_test, pred):
        confusion = confusion_matrix(y_test, pred)
        acc_score = accuracy_score(y_test, pred)
        re_score = recall_score(y_test, pred)
        pre_score = precision_score(y_test, pred)
        f1 = f1_score(y_test, pred)
        print('오차행렬')
        print(confusion)
        print(f'\n정확도 : {acc_score}\n정밀도 : {pre_score}\n재현율 : {re_score}\nf1 : {f1}')

    
    def get_score_list(y_test, pred, thr):
        for thr in thr:
            binarizer = Binarizer(threshold=thr).fit(pred)
            custom_predict = binarizer.transform(pred)
            print(f'\n임계값 : {thr}')
            get_score(y_test, custom_predict)

    
    custom_thr = [0.1, 0.15, 0.2, 0.25, 0.3]
    pred = model.predict_proba(X_val)
    y_pred = pred[:, 1].reshape(-1, 1)
    get_score_list(y_val, y_pred, custom_thr)