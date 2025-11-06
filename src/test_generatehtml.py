import unittest
from generatepages import extract_title

class TestGenerateHtml(unittest.TestCase):
    def test_extract_title(self):
        title = extract_title("# This is a title")
        self.assertEqual("This is a title", title)
        
    def test_extract_title_error(self):
        with self.assertRaises(Exception):
            title = extract_title("This is not a title")