import unittest
from parse import *
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
            
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)
    
    def test_extract_matches_links_excl_images(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_matches_images_excl_links(self):
        matches = extract_markdown_images(
            "This is text with a [link](https://www.boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_mult(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ![second image](https://i.imgur.com/3elNhQu.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"), 
                ("second image", "https://i.imgur.com/3elNhQu.png")
            ],
        matches)

    def test_extract_markdown_links_mult(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com) and a [second link](https://www.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://www.google.com"), 
                ("second link", "https://www.boot.dev")
            ],
        matches)
        
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode(
            "This is text without an image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text without an image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.google.com"
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode(
            "This is text without a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text without a link", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_text_to_text_nodes(self):
        print("\n")
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        
        nodes = text_to_text_nodes(text)
        # self.assertListEqual(
        #     [
        #         TextNode("This is ", TextType.TEXT),
        #         TextNode("text", TextType.BOLD),
        #         TextNode(" with an ", TextType.TEXT),
        #         TextNode("italic", TextType.ITALIC),
        #         TextNode(" word and a ", TextType.TEXT),
        #         TextNode("code block", TextType.CODE),
        #         TextNode(" and an ", TextType.TEXT),
        #         TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        #         TextNode(" and a ", TextType.TEXT),
        #         TextNode("link", TextType.LINK, "https://boot.dev"),
        #     ],
        #     nodes,
        # )


if __name__ == "__main__":
    unittest.main()