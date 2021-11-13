from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/predict",  methods=['POST'])
def predict():
    data = request.form.get('data')
    print(data)
    resp = {
        'answer': 1,
    }
    
    return resp


@app.route("/result_question",  methods=['POST'])
def result_question():
    data = request.form.get('data')
    print(data)
    return {'data': 'ok'}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12300, debug=True)
