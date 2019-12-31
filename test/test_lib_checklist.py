import unittest
import json

import main
from main.lib.checklist import Checklist


class TestLibChecklist(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # healthcheck.py
    def test_get_chacklist_templates(self):
        text = '''
# comment
# h2 comment
 # Irregular comments
.* DEFAULT.md
.*.py SERVERSIDE_CHECKLIST.md
.*.md MARKDOWN_CHECKLIST.md #end comment no error
  .*.aa IRREGULAR.md

'''
        checklist = Checklist()
        result = checklist._get_chacklist_templates(text)
        print(result)
        answer_data = {
            '.*.py': 'SERVERSIDE_CHECKLIST.md',
            '.*.md': 'MARKDOWN_CHECKLIST.md',
            '.*.aa': 'IRREGULAR.md',
            '.*': 'DEFAULT.md'
        }
        # Can be in any order
        self.assertDictEqual(result, answer_data)


if __name__ == '__main__':
    unittest.main()
