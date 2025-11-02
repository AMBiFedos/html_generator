from textnode import TextNode, TextType
from htmlnode import LeafNode, HtmlTag
import re

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
    pattern = r"(?:!)(?:\[)(.+?)(?:\])(?:\()(\w+?://.+?)(?:\))"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?:[^!])(?:\[)(.+?)(?:\])(?:\()(\w+?://.+?)(?:\))"
    return re.findall(pattern, text)

