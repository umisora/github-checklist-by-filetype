from main.lib.webhook_runner.base_runner import BaseRunner
from main.lib.client.github import GithubClient
from main.lib.checklist import Checklist


class Runner(BaseRunner):
    def __init__(self, payload):
        super().__init__(payload)
        print('Initilize Pull Request Runnner.')
        self.CHECKLIST_HEADER = '\n\n---- \n### CHECKLIST\n'
        self.CHECKLIST_FOOTER = '\nby [umisora/github-checklist-by-filetype](https://github.com/umisora/github-checklist-by-filetype)'
        self.HOOK_EVENT_LIST = ['opened', 'reopened', 'synchronize']

        self.action = self.payload['action']
        self.pull_number = self.payload['pull_request']['number']
        self.change_files_count = self.payload['pull_request']['changed_files']
        self.reponame = self.payload['pull_request']['head']['repo']['full_name']
        self.description = self.payload['pull_request']['body']
        self.checklists_contains = self.CHECKLIST_HEADER in self.description
        self.client = GithubClient()

    def run(self):
        print('Start Pull Request Webhook Runner.')

        # Validation
        if self.change_files_count == 0 or \
                self.action not in self.HOOK_EVENT_LIST:
            return "Skip request."

        print("PR Parameter", self.action, self.pull_number,
              self.change_files_count)

        # Update if description are any changes.
        new_description = self._description_builder()
        if not new_description == self.description:
            print(
                "Update description for #" + str(self.pull_number),
                "\n[before]:\n",
                self.description,
                "\n[after]:\n",
                new_description
            )
            self.client.update_pr_description(
                self.reponame, self.pull_number, new_description)

        return "Updated checklist"

    def _description_builder(self):
        new_description = self.description
        checklist_content = ""

        # Add header for the first time
        if not self.checklists_contains:
            checklist_content = self.CHECKLIST_HEADER

        # Select the checklist to use
        template_count = 0
        checklists = Checklist.get_by_file_match(
            self._get_files(), self.reponame)
        for template_name in checklists:
            # Skip if already used
            if template_name in self.description:
                continue

            # Build a checklist
            checklist_content = '\n'.join([
                checklist_content,
                "**■ " + template_name + "**",
                self.client.get_github_object(
                    self.reponame, ".github/" + template_name
                ),
                '\n'
            ])
            template_count += 1

        # Add footer
        if template_count > 0:
            new_description = self.description.replace(
                self.CHECKLIST_FOOTER, '', 1).strip() +\
                checklist_content + self.CHECKLIST_FOOTER

        return new_description

    def _get_files(self):
        return self.client.get_files_of_pr(self.reponame, self.pull_number)
