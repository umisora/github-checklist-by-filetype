import os
import urllib.request
import json


class GithubClient():
    def __init__(self):
        self.github_token = os.getenv(
            'GITHUB_PERSONAL_ACCESS_TOKEN', 'dummy')
        self.github_base_url = os.getenv(
            'GITHUB_BASEURL', 'https://api.github.com')
        self.auth_header = {"Authorization": "token " + self.github_token}

    def get_github_object(self, reponame, filename):
        print(self.github_base_url + "/repos/" + reponame + "/contents/" +
              filename + "?ref=master")
        request = urllib.request.Request(
            self.github_base_url + "/repos/" + reponame + "/contents/" +
            filename + "?ref=master",
            None,
            self.auth_header
        )
        print(request)
        response = urllib.request.urlopen(request)

        file_meta = json.loads(response.read().decode("utf-8"))
        file = urllib.request.urlopen(
            file_meta['download_url']
        ).read().decode("utf-8")
        # print("get checklist¥n", file)
        return file

    # /repos/:owner/:repo/pulls/:pull_number/files
    def get_files_of_pr(self, repo_name, pull_number):
        request = urllib.request.Request(
            self.github_base_url + "/repos/" + repo_name +
            "/pulls/" + str(pull_number) + "/files",
            None,
            self.auth_header
        )
        response = urllib.request.urlopen(request)
        files = json.loads(response.read().decode("utf-8"))
        pr_file_list = []
        for file in files:
            pr_file_list.append(file['filename'])

        return pr_file_list

    def get_pr_description(self, repo_name, pull_number):
        request = urllib.request.Request(
            self.github_base_url + "/repos/" + repo_name +
            "/pulls/" + str(pull_number),
            None,
            self.auth_header
        )
        response = urllib.request.urlopen(request)
        json_data = json.loads(response.read().decode("utf-8"))
        description = json_data['body']
        return description

    def update_pr_description(self, repo_name, pull_number, description):
        patch_parameter = {}
        patch_parameter['body'] = description
        request = urllib.request.Request(
            self.github_base_url + "/repos/" + repo_name +
            "/pulls/" + str(pull_number),
            json.dumps(patch_parameter).encode(),
            self.auth_header,
            method='PATCH'
        )
        response = urllib.request.urlopen(request)
        if response.status != 200:
            print("更新に失敗しました")
            return "ERR"

        print("更新に成功しました")
        return "OK"
