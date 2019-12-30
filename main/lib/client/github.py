import os
import urllib.request
import json


class GithubClient():
    def get_github_object(self, reponame, filename):
        request = GithubRequest(
            "/repos/" + reponame + "/contents/" + filename + "?ref=master"
        )
        response = urllib.request.urlopen(request)

        file_meta = json.loads(response.read().decode("utf-8"))
        file = urllib.request.urlopen(file_meta['download_url'])

        return file.read().decode("utf-8")

    def get_files_of_pr(self, repo_name, pull_number):
        request = GithubRequest(
            "/repos/" + repo_name + "/pulls/" + str(pull_number) + "/files"
        )
        response = urllib.request.urlopen(request)

        files = json.loads(response.read().decode("utf-8"))
        pr_file_list = []
        for file in files:
            pr_file_list.append(file['filename'])

        return pr_file_list

    def update_pr_description(self, repo_name, pull_number, description):
        patch_parameter = {}
        patch_parameter['body'] = description
        request = GithubRequest(
            "/repos/" + repo_name + "/pulls/" + str(pull_number),
            json.dumps(patch_parameter).encode(),
            method='PATCH'
        )
        response = urllib.request.urlopen(request)
        if response.status != 200:
            print("更新に失敗しました")
            return "ERR"

        print("更新に成功しました")
        return "OK"


class GithubRequest(urllib.request.Request):
    def __init__(self, url, data=None, headers={},
                 origin_req_host=None, unverifiable=False,
                 method=None):

        self.github_token = os.getenv(
            'GITHUB_PERSONAL_ACCESS_TOKEN', 'dummy')
        self.github_base_url = os.getenv(
            'GITHUB_BASEURL', 'https://api.github.com')
        self.auth_header = {"Authorization": "token " + self.github_token}

        headers.update(self.auth_header)
        url = self.github_base_url + url

        super().__init__(url, data, headers,
                         origin_req_host, unverifiable,
                         method)
