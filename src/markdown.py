from textnode import TextNode, TextType
from htmlnode import LeafNode, HtmlTag
import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "para"
    HEADING = "head"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "ulist"
    ORDERED_LIST = "olist"


def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("Invalid TextType")

    text = text_node.text
    props = None
    
    match text_node.text_type.name:
        case "TEXT":
            tag = None
        case "BOLD":
            tag = HtmlTag.BOLD.value
        case "ITALIC":
            tag = HtmlTag.ITALIC.value
        case "CODE":
            tag = HtmlTag.CODE.value
        case "LINK":
            tag = HtmlTag.LINK.value
            props = {"href": text_node.url}
        case "IMAGE":
            tag = HtmlTag.IMAGE.value
            text = ""
            props = {"src": text_node.url, "alt": text}
        case _:
            raise Exception("Invalid TextType")
    
    return LeafNode(tag, text, props)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        delimiter_count = node.text.count(delimiter)
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter_count == 0:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
            continue
        if delimiter_count % 2 != 0:
            raise ValueError("TextNode contains mismatched delimiters")
        
        
        text_split = node.text.split(delimiter)
        modulo = 1 if node.text[0] == delimiter else 0
        for i, split in enumerate(text_split):
            type = TextType.TEXT if i % 2 == modulo else text_type
                
            new_node = TextNode(split, type)
            new_nodes.append(new_node)
            
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes






# def split_nodes_image(old_nodes):
#     new_nodes = []
    
#     for node in old_nodes:
#         text = node.text
#         images = extract_markdown_images(text)
#         if len(images) == 0:
#             new_nodes.append(node)
            
#         for image in images:
#             sections = text.split(f"![{image[0]}]({image[1]})", 1)
            
#             if len(sections[0]) > 0:
#                 new_nodes.append(
#                     TextNode(sections[0], node.text_type)
#                 )
            
#             new_nodes.append(
#                 TextNode(image[0], TextType.IMAGE, image[1])
#             )
            
#             text = sections[1]
    
#     return new_nodes

# def split_nodes_link(old_nodes):
#     new_nodes = []
    
#     for node in old_nodes:
#         text = node.text
#         links = extract_markdown_links(text)
#         if len(links) == 0:
#             new_nodes.append(node)
            
#         for link in links:
#             sections = text.split(f"[{link[0]}]({link[1]})", 1)
#             if len(sections[0]) > 0:
#                 new_nodes.append(
#                     TextNode(sections[0], node.text_type)
#                 )
            
#             new_nodes.append(
#                 TextNode(link[0], TextType.LINK, link[1])
#             )
            
#             text = sections[1]
    
#     return new_nodes

def text_to_text_nodes(text):
    text_nodes = [
        TextNode(text, TextType.TEXT)
    ]

    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes

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