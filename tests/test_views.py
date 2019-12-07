import unittest
import json
from main import views


class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = views.app.test_client()

    def test_post(self):
        response = self.app.post('/webhook/github/pullrequest',
                       data=json.dumps(dict(hoge='foo', fuga='bar')),
                       content_type='application/json',
                       headers={'X-Hub-Signature': 'dummy'})
        self.assertEqual(response.status_code, 200)

    def test_post_fail(self):
        response = self.app.post('/webhook/github/pullrequest',
                       data=json.dumps(dict(hoge='foo', fuga='bar')),
                       content_type='application/json',
                       headers={'X-Hub-Signature': 'fail'})
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
