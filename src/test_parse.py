import unittest
from parse import text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType
from htmlnode import LeafNode

class TestParse(unittest.TestCase):
    def test_to_html_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_to_html_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_to_html_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_split_single_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        desired = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
            ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), desired)

    def test_split_no_delimiter(self):
        node = TextNode("This is text with no markdown.", TextType.TEXT)
        desired = [TextNode("This is text with no markdown.", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), desired)

    def test_split_not_text_type(self):
        node = TextNode("This is text with no markdown.", TextType.BOLD)
        desired = [TextNode("This is text with no markdown.", TextType.BOLD)]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), desired)
        
    def test_split_mismatch_markdown(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

if __name__ == "__main__":
    unittest.main()