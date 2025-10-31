import unittest
from htmlnode import HtmlNode, LeafNode

class TestHtmlNode(unittest.TestCase):
    def test_base_to_html_not_implemented(self):
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
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")
        
    def test_leaf_to_html_blockquote(self):
        node = LeafNode("blockquote", 
                        "A LeafNode is a type of HTMLNode that represents a single HTML tag with no children. For example, a simple <p> tag with some text inside of it",
                        {"cite": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), "<blockquote>A LeafNode is a type of HTMLNode that represents a single HTML tag with no children. For example, a simple <p> tag with some text inside of it</blockquote>")
        
    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)
        
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello world")
        self.assertEqual(node.to_html(), "Hello world")