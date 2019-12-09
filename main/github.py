import os
from github import Github
import urllib.request
import json


class GithubClient():
    def __init__(self):
        self.github_token = os.getenv(
            'GITHUB_PERSONAL_ACCESS_TOKEN', 'dummy')
        self.github_base_url = os.getenv(
            'GITHUB_BASEURL', 'https://api.github.com')
        self.auth_header = {"Authorization": "token " + self.github_token}

    def get_github_object(self, filename):
        request = urllib.request.Request(
            self.github_base_url + "/repos/umisora/github-checklist-by-filetype/contents/" + filename + "?ref=master", None, self.auth_header)
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
        description = json_data['head']['repo']['description']
        return description
