import unittest
from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
    def test_to_html_not_implemented(self):
        node = HtmlNode("p", "This is an HTML node")
        self.assertRaises(NotImplementedError, node.to_html)
        
    def test_props_to_html_a(self):
        node = HtmlNode("a", "This is an HTML node", None, {"href": "https://www.boot.dev", "target": "_blank"})
        html_props = ' href="https://www.boot.dev" target="_blank"'
        self.assertEqual(node.props_to_html(), html_props)
    
    def test_props_to_html_img(self):
        node = HtmlNode("img", None, None, {"src": "https://imgur.com/gallery/cat-trap-worked-onlto8M#/t/cat", 
                                            "alt": "photo of a cat sitting in a cardboard box"})
        html_props = ' src="https://imgur.com/gallery/cat-trap-worked-onlto8M#/t/cat" alt="photo of a cat sitting in a cardboard box"'
        self.assertEqual(node.props_to_html(), html_props)
    
