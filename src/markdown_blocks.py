from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(markdown_block):
    if len(re.findall(r"(^#{1,6} )", markdown_block)) > 0:
        return BlockType.HEADING
    
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    
    if len(re.findall(r"(?m)(^>)", markdown_block)) > 0:
        return BlockType.QUOTE
    
    if len(re.findall(r"(?m)(^- )", markdown_block)) > 0:
        return BlockType.UNORDERED_LIST
    
    if len(re.findall(r"(?m)(\d+. )", markdown_block)) > 0:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH