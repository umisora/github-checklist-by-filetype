import unittest
import json
import main


class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = main.app.test_client()

    def test_ping(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        request_data = "test/sample-webhook/sample-webhook-pr-open.json"
        post_endpoint = "/webhook/github/pullrequest?token=dummy"
        response = self.app.post(
            post_endpoint,
            data=open(request_data, 'r'),
            content_type='application/json',
            headers={'X-Hub-Signature': 'dummy'}
        )
        self.assertEqual(response.status_code, 200)

    def test_post_fail(self):
        request_data = "test/sample-webhook/sample-webhook-pr-open.json"
        post_endpoint = "/webhook/github/pullrequest?token=fail"
        response = self.app.post(
            post_endpoint,
            data=open(request_data, 'r'),
            content_type='application/json',
            headers={'X-Hub-Signature': 'fail'}
        )
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
