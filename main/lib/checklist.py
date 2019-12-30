import re
from main.lib.client.github import GithubClient


class Checklist():
    @classmethod
    def get_by_file_match(self, files: list, reponame: str):
        CHECKLIST_PATH = '.github/CHECKLIST'
        client = GithubClient()
        checklist_templates = self._get_chacklist_templates(
            self,
            client.get_github_object(reponame, CHECKLIST_PATH)
        )

        # file match
        template_list = []
        for regexp, template_name in checklist_templates.items():
            for filename in files:
                if re.match(regexp, filename):
                    # print("Match!!", filename, regexp, template_name)
                    template_list.append(template_name)
        # 重複排除
        unique_template_list = list(set(template_list))
        print(unique_template_list)
        return unique_template_list

    def _get_chacklist_templates(self, checklist: str) -> dict:
        checklist_dict = {}
        for line in checklist.splitlines():
            key = line.split()[0]
            value = line.split()[1]
            checklist_dict[key] = value

        return checklist_dict
