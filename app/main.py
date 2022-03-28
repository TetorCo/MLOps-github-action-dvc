from flask import Flask, render_template, request
# from sklearn.preprocessing import Binarizer
import pickle


app = Flask(__name__)
model = None


@app.route('/')
def main():
    return render_template('main.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)