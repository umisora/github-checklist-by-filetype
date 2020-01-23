import os
import json
import requests


class GithubClient():
    def __init__(self):
        self.github_token = os.getenv(
            'GITHUB_PERSONAL_ACCESS_TOKEN', 'dummy')
        self.github_base_url = os.getenv(
            'GITHUB_BASEURL', 'https://api.github.com')
        self.auth_header = {"Authorization": "token " + self.github_token}

    def get_github_object(self, reponame, filename):
        response = requests.get(
            self.github_base_url + "/repos/" + reponame +
            "/contents/" + filename + "?ref=master",
            headers=self.auth_header
        )
        raw_file = requests.get(
            response.json()['download_url'], headers=self.auth_header).text

        return raw_file

    def get_files_of_pr(self, repo_name, pull_number):
        response = requests.get(
            self.github_base_url + "/repos/" + repo_name +
            "/pulls/" + str(pull_number) + "/files",
            headers=self.auth_header
        )
        if response.status_code != 200:
            raise RuntimeError(
                'Get files of PR is failed.' + str(response.json()))

        files = response.json()
        print(files)
        pr_file_list = []
        for file in files:
            pr_file_list.append(file['filename'])

        return pr_file_list

    def update_pr_description(self, repo_name, pull_number, description):
        parameter = {'body': description}
        response = requests.patch(
            self.github_base_url + "/repos/" +
            repo_name + "/pulls/" + str(pull_number),
            json=json.dumps(parameter),
            headers=self.auth_header
        )
        if response.status_code != 200:
            raise RuntimeError(
                'Update PR description is fail.' + str(response.json()))

        print("更新に成功しました")
        return "OK"
