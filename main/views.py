import os
import json
import re
from flask import Flask, jsonify, request
from main.github import GithubClient

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
        # get webhook data
        print("signature:", signature)
        PULL_ACTION = payload_dict['action']
        PULL_NUMBER = payload_dict['pull_request']['number']
        NEXT_LINK = payload_dict['pull_request']['_links']['self']['href']
        CHANGE_FILES_COUNT = payload_dict['pull_request']['changed_files']
        REPONAME = payload_dict['pull_request']['head']['repo']['full_name']
        print("PR Parameter", PULL_ACTION, PULL_NUMBER,
              NEXT_LINK, CHANGE_FILES_COUNT)
        if CHANGE_FILES_COUNT == 0:
            print("skip because change file count is Zero")
            return "skip because change file count is Zero", 200

        client = GithubClient()

        # get checklist
        checklist = client.get_checklist()
        checklist_dict = {}
        for line in checklist.splitlines():
            key = line.split()[0]
            value = line.split()[1]
            checklist_dict[key] = value

        print(checklist_dict)

        # get filenames
        filenames = client.get_files_of_pr(REPONAME, PULL_NUMBER)
        print(filenames)

        # file match
        template_list = []
        for regexp, template_name in checklist_dict.items():
            for filename in filenames:
                if re.match(regexp, filename):
                    print("Match!!", filename, regexp, template_name)
                    template_list.append(template_name)

        print(set(template_list))
        return "", 200


if __name__ == '__main__':
    app.run(debug=True)
