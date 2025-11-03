import unittest
from markdown_blocks import *


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading1(self):
        markdown = "# This is a heading"
        block_type = block_to_block_type(markdown)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_heading1(self):
        markdown = "# This is a heading"
        block_type = block_to_block_type(markdown)
        self.assertEqual(BlockType.HEADING, block_type)
    
    def test_block_to_block_type_code_one_line(self):
        markdown = "```This is a one-line code block```"
        block_type = block_to_block_type(markdown)
        self.assertEqual(BlockType.CODE, block_type)
    
    def test_block_to_block_type_code_multi_line(self):
        markdown = """```This is a the first line of a multi-line code block.
This is the second line.```"""
        block_type = block_to_block_type(markdown)
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_to_block_type_quote(self):    
        markdown = """>This is a the first line of a quote block.
>This is the second line."""
        markdown = markdown.strip()
        block_type = block_to_block_type(markdown)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_to_block_type_unordered(self):    
        markdown = """- This is a the first line of an unordered list.
- This is the second line.```"""
        block_type = block_to_block_type(markdown)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_block_to_block_type_ordered(self):    
        markdown = """1. This is a the first line of an ordered list.
2. This is the second line.```"""
        block_type = block_to_block_type(markdown)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)


if __name__ == "__main__":
    unittest.main()