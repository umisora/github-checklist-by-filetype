from main import app

import os
import json
import re
from flask import jsonify, request
from main.lib.github import GithubClient

GITHUB_WEBHOOK_SECRET_TOKEN = os.getenv('GITHUB_WEBHOOK_SECRET_TOKEN', "dummy")


@app.route('/webhook/github/pullrequest', methods=['POST'])
def webhook_github_pullrequest():
    print("********** Hello API *************")
    HOOK_EVENT_LIST = ['opened', 'reopened', 'synchronize']

    body = request.get_data().decode('utf-8')
    signature = request.args.get('token')
    # signature = request.headers.get('X-Hub-Signature')
    payload_dict = json.loads(body)
    payload_action = payload_dict['action']
    payload_pull_number = payload_dict['pull_request']['number']
    payload_next_link = payload_dict['pull_request']['_links']['self']['href']
    payload_change_files_count = payload_dict['pull_request']['changed_files']
    payload_reponame = payload_dict['pull_request']['head']['repo']['full_name']
    pauload_description = payload_dict['pull_request']['body']

    if not __verify_request_signature(signature):
        "Signature is UnMatch.", 401
    if payload_change_files_count == 0 | payload_action not in HOOK_EVENT_LIST:
        return "Skip request.", 200

    print("PR Parameter", payload_action, payload_pull_number,
          payload_next_link, payload_change_files_count)

    client = GithubClient()

    # get checklist
    checklist = client.get_github_object(payload_reponame, ".github/CHECKLIST")
    checklist_dict = {}
    for line in checklist.splitlines():
        key = line.split()[0]
        value = line.split()[1]
        checklist_dict[key] = value

    print(checklist_dict)

    # get filenames
    filenames = client.get_files_of_pr(payload_reponame, payload_pull_number)
    print(filenames)

    # file match
    template_list = []
    for regexp, template_name in checklist_dict.items():
        for filename in filenames:
            if re.match(regexp, filename):
                # print("Match!!", filename, regexp, template_name)
                template_list.append(template_name)
    # 重複排除
    unique_template_list = list(set(template_list))
    print(unique_template_list)

    # template filesの中身を取得する
    CHECKLIST_HEADER = '\n\n---- \n### CHECKLIST\n'
    CHECKLIST_FOOTER = '\nby [umisora/github-checklist-by-filetype](https://github.com/umisora/github-checklist-by-filetype)'

    # 初回だけ
    if payload_action == "opened":
        checklist_content = CHECKLIST_HEADER

    join_count = 0
    for filename in unique_template_list:
        # checklistが既に含まれていたらskip
        print("FileName:", filename)
        if filename in pauload_description:
            continue

        # 含まれていなければjoin
        join_count += 1
        checklist_content = '\n'.join([
            checklist_content,
            "**■ " + filename + "**"
        ])

        checklist_content = '\n'.join([
            checklist_content,
            client.get_github_object(payload_reponame, ".github/" + filename)
        ])
        checklist_content = checklist_content + '\n'

    if join_count == 0:
        print("更新内容がないのでUpdateをSkipします")
        return "", 200

    # 更新がある場合、末尾にChecklistを追加する
    # その際にFooterをつけ直す
    print(checklist_content)
    new_description = pauload_description.replace(
        CHECKLIST_FOOTER, '', 1).strip() + checklist_content + CHECKLIST_FOOTER
    print(new_description)

    # 更新が1件でもあったらUpdateする
    client.update_pr_description(
        payload_reponame, payload_pull_number, new_description)
    return "", 200


def __verify_request_signature(self, signature):
    if signature != GITHUB_WEBHOOK_SECRET_TOKEN:
        print("Token is UnMatch")
        return False
    else:
        print("Token is Match")
        return True
