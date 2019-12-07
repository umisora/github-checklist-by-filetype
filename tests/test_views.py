import unittest
import json
from flask import jsonify
from main import views


class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = views.app.test_client()

    def test_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Hello, World!')

    def test_get02(self):
        response = self.app.get('/hello')
        self.assertEqual(response.status_code, 200)
        json_data = response.data.decode('utf-8')
        di = json.loads(json_data)
        self.assertEqual(di['message'], 'Hello, world')


if __name__ == '__main__':
    unittest.main()
