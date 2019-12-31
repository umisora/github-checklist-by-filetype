import unittest
import json

import main
import main.view.api as webhook


class TestViewsHealthCheck(unittest.TestCase):

    def setUp(self):
        self.app = main.app.test_client()
        pass

    def tearDown(self):
        pass

    # healthcheck.py
    def test_ping(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
