import os
from github import Github
import urllib.request
import json


class GithubClient():
    def __init__(self):
        self.github_token = os.getenv(
            'GITHUB_PERSONAL_ACCESS_TOKEN', 'fb823ebccc48c6dbb792be7a8f49deda2f7d8be6')
        self.github_base_url = os.getenv(
            'GITHUB_BASEURL', 'https://api.github.com')
        self.client = Github(login_or_token=self.github_token,
                             base_url=self.github_base_url)

    def get_checklist(self):
        response = urllib.request.urlopen(
            "https://api.github.com/repos/umisora/github-checklist-by-filetype/contents/.github/CHECKLIST?ref=master"
        )
        file_meta = json.loads(response.read().decode("utf-8"))
        file = urllib.request.urlopen(
            file_meta['download_url']
        ).read().decode("utf-8")
        #print("get checklist¥n", file)
        return file

    def get_checklist_template(self):
        print("get checklist template")

    # /repos/:owner/:repo/pulls/:pull_number/files
    def get_files_of_pr(self, repo_name, pr_number):
        response = urllib.request.urlopen(
            "https://api.github.com/repos/" + repo_name +
            "/pulls/" + str(pr_number) + "/files"
        )
        files = json.loads(response.read().decode("utf-8"))
        pr_file_list = []
        for file in files:
            pr_file_list.append(file['filename'])

        return pr_file_list
