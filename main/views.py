
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return 'Hello, World!', 200


@app.route('/hello', methods=['GET'])
def hello_json():
    return jsonify({'message': 'Hello, world'})


if __name__ == '__main__':
    app.run(debug=True)
