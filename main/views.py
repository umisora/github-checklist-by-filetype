import os
import json
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

GITHUB_WEBHOOK_SECRET_TOKEN = os.getenv('GITHUB_WEBHOOK_SECRET_TOKEN', "dummy")


@app.route('/', methods=['GET'])
def ping():
    return "Hello World", 200


@app.route('/webhook/github/pullrequest', methods=['POST'])
def webhook_github_pullrequest():
    print("********** Hello API *************")
    body = request.get_data().decode('utf-8')
    payload_dict = json.loads(body)
    print(payload_dict)
    signature = request.headers.get('X-Hub-Signature')
    if signature != GITHUB_WEBHOOK_SECRET_TOKEN:
        print("signature:", signature)
        return "", 403
    else:
        print("signature:", signature)
        PULL_ACTION = payload_dict['pull_request']['state']
        PULL_NUMBER = payload_dict['pull_request']['number']
        NEXT_LINK = payload_dict['pull_request']['base']['_links']['self']['href']
        CHANGE_FILES_COUNT = payload_dict['pull_request']['changed_files']
        print("PR Parameter", PULL_ACTION, PULL_NUMBER,
              NEXT_LINK, CHANGE_FILES_COUNT)
        return "", 200


if __name__ == '__main__':
    app.run(debug=True)
