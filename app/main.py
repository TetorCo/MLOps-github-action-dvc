from flask import Flask, render_template, request
from sklearn.preprocessing import Binarizer
import pickle


app = Flask(__name__)
model = None


@app.route('/')
def main():
    return render_template('main.html')



@app.route('/fw', methods=['GET','POST'])
def fw_predict():
    with open('model_fw.pkl', 'rb') as model_fw:
        model = pickle.load(model_fw)

    apperances = request.form['출전한리그경기수']
    goals = request.form['골']
    assist = request.form['도움']
    bcm = request.form['빅찬스미스']

    pred = model.predict_proba(
        [[apperances, goals, assist, bcm]]
    )
    y_pred = pred[:, 1].reshape(-1, 1)
    binarizer = Binarizer(threshold=0.2).fit(y_pred)
    custom_pred = binarizer.transform(y_pred)
    return render_template('predict.html', data=custom_pred)


@app.route('/mf', methods=['GET','POST'])
def mf_predict():
    with open('model_mf.pkl', 'rb') as model_mf:
        model = pickle.load(model_mf)

    apperances = request.form['출전한리그경기수']
    goals = request.form['골']
    assist = request.form['도움']
    bcc = request.form['기회창출']

    pred = model.predict_proba(
        [[apperances, goals, assist, bcc]]
    )
    y_pred = pred[:, 1].reshape(-1, 1)
    binarizer = Binarizer(threshold=0.2).fit(y_pred)
    custom_pred = binarizer.transform(y_pred)
    return render_template('predict.html', data=custom_pred)


@app.route('/df', methods=['GET','POST'])
def df_predict():
    with open('model_df.pkl', 'rb') as model_df:
        model = pickle.load(model_df)

    apperances = request.form['출전한리그경기수']
    blocks = request.form['슈팅을막은횟수']
    pass_per_match = request.form['경기당패스횟수']
    passes = request.form['패스횟수']

    pred = model.predict_proba(
        [[apperances, blocks, pass_per_match, passes]]
    )
    y_pred = pred[:, 1].reshape(-1, 1)
    binarizer = Binarizer(threshold=0.85).fit(y_pred)
    custom_pred = binarizer.transform(y_pred)
    return render_template('predict.html', data=custom_pred)


@app.route('/gk', methods=['GET','POST'])
def gk_predict():
    with open('model_gk.pkl', 'rb') as model_gk:
        model = pickle.load(model_gk)

    apperances = request.form['출전한리그경기수']
    saves = request.form['무실점']
    pen_saves = request.form['롱볼']
    high_claims = request.form['자책골']


    pred = model.predict_proba(
        [[apperances, saves, pen_saves, high_claims]]
    )
    y_pred = pred[:, 1].reshape(-1, 1)
    binarizer = Binarizer(threshold=0.1).fit(y_pred)
    custom_pred = binarizer.transform(y_pred)
    return render_template('predict.html', data=custom_pred)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)