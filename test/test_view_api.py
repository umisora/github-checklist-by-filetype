import unittest
from unittest.mock import Mock, patch
import pook
import json

import main
import main.view.api as webhook


class TestViewApi(unittest.TestCase):

    def setUp(self):
        self.app = main.app.test_client()
        pass

    def tearDown(self):
        pass

    @pook.on
    def test_webhook_github(self):
        # Mocks
        # method: GET
        mock_list = [
            {
                'url': 'https://api.github.com/repos/umisora/github-checklist-by-filetype/contents/.github/CHECKLIST?ref=master',
                'response_type': 'json',
                'method': 'GET',
                'response_body': 'test/sample-webhook/sample-response/get_github_object-github-CHECKLIST.json'
            },
            {
                'url': 'https://api.github.com/repos/umisora/github-checklist-by-filetype/contents/.github/DEFAULT.md',
                'response_type': 'json',
                'method': 'GET',
                'response_body': 'test/sample-webhook/sample-response/get_github_object-github-DEFAULTmd.json'
            },
            {
                'url': 'https://api.github.com/repos/umisora/github-checklist-by-filetype/contents/.github/SERVERSIDE_CHECKLIST.md',
                'response_type': 'json',
                'method': 'GET',
                'response_body': 'test/sample-webhook/sample-response/get_github_object-github-SERVERSIDE_CHECKLISTmd.json'
            },
            {
                'url': 'https://raw.githubusercontent.com/umisora/github-checklist-by-filetype/master/.github/CHECKLIST',
                'response_type': 'text/plai',
                'method': 'GET',
                'response_body': 'test/sample-webhook/sample-response/get_github_object-github-CHECKLIST-raw.txt'
            },
            {
                'url': 'https://raw.githubusercontent.com/umisora/github-checklist-by-filetype/master/.github/DEFAULT.md',
                'response_type': 'text/plain',
                'method': 'GET',
                'response_body': 'test/sample-webhook/sample-response/get_github_object-github-DEFAULTmd-raw.txt'
            },
            {
                'url': 'https://raw.githubusercontent.com/umisora/github-checklist-by-filetype/master/.github/SERVERSIDE_CHECKLIST.md',
                'response_type': 'text/plain',
                'method': 'GET',
                'response_body': 'test/sample-webhook/sample-response/get_github_object-github-SERVERSIDE_CHECKLISTmd-raw.txt'
            },
            {
                'url': 'https://api.github.com/repos/umisora/github-checklist-by-filetype/pulls/1/files',
                'response_type': 'json',
                'method': 'GET',
                'response_body': 'test/sample-webhook/sample-response/get_files_of_pr.json'
            },
            {
                'url': 'https://api.github.com/repos/umisora/github-checklist-by-filetype/pulls/1',
                'response_type': 'json',
                'method': 'PATCH',
                'response_body': 'test/sample-webhook/sample-response/update_pr_description.json'
            },
        ]
        mocks = []
        for mock in mock_list:
            mocks.append(pook.mock(
                mock['url'],
                method=mock['method'],
                reply=200,
                response_type=mock['response_type'],
                response_body=open(mock['response_body'], 'r').read()
            ))

        # Test
        request_data = "test/sample-webhook/sample-webhook-pr-open.json"
        post_endpoint = "/webhook/github?token=dummy"
        response = self.app.post(
            post_endpoint,
            data=open(request_data, 'r'),
            content_type='application/json',
            headers={'X-Hub-Signature': 'dummy',
                     'X-GitHub-Event': 'pull_request'}
        )
        for mock in mocks:
            print("mock call count is ", mock.calls)

        self.assertEqual(response.status_code, 200)

    def test_verify_request_signature_success(self):
        self.assertEqual(webhook._verify_request_signature('dummy'), True)

    def test_verify_request_signature_fail(self):
        self.assertEqual(webhook._verify_request_signature('fail'), False)


if __name__ == '__main__':
    unittest.main()
