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
        HOOK_EVENT_LIST = ['opened', 'reopened', 'synchronize']

        print("PR Parameter", PULL_ACTION, PULL_NUMBER,
              NEXT_LINK, CHANGE_FILES_COUNT)
        if CHANGE_FILES_COUNT == 0:
            print("skip because change file count is Zero")
            return "skip because change file count is Zero", 200
        if PULL_ACTION not in HOOK_EVENT_LIST:
            print("skip because pull action is not in hook event list")
            return "skip because pull action is not in hook event list", 200

        client = GithubClient()

        # get checklist
        checklist = client.get_github_object(".github/CHECKLIST")
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
                    # print("Match!!", filename, regexp, template_name)
                    template_list.append(template_name)
        # 重複排除
        unique_template_list = list(set(template_list))
        print(unique_template_list)

        # 現在のPRのDescriptionを取得する
        description = client.get_pr_description(REPONAME, PULL_NUMBER)
        # print(description)

        # template filesの中身を取得する
        CHECKLIST_HEADER = '\n\n---- \n### CHECKLIST\n'
        CHECKLIST_FOOTER = '\nby [umisora/github-checklist-by-filetype](https://github.com/umisora/github-checklist-by-filetype)'

        # 初回だけ
        if PULL_ACTION == "opened":
            checklist_content = CHECKLIST_HEADER

        join_count = 0
        for filename in unique_template_list:
            # checklistが既に含まれていたらskip
            print("FileName:", filename)
            if filename in description:
                continue

            # 含まれていなければjoin
            join_count += 1
            checklist_content = '\n'.join([
                checklist_content,
                "**■ " + filename + "**"
            ])

            checklist_content = '\n'.join([
                checklist_content,
                client.get_github_object(".github/" + filename)
            ])
            checklist_content = checklist_content + '\n'

        if join_count == 0:
            print("更新内容がないのでUpdateをSkipします")
            return "", 200

        # 更新がある場合、末尾にChecklistを追加する
        # その際にFooterをつけ直す
        print(checklist_content)
        new_description = description.replace(
            CHECKLIST_FOOTER, '', 1).strip() + checklist_content + CHECKLIST_FOOTER
        print(new_description)

        # 更新が1件でもあったらUpdateする
        client.update_pr_description(REPONAME, PULL_NUMBER, new_description)
        return "", 200
