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
    pattern = r"(?:[^!]|^)(?:\[)(.+?)(?:\])(?:\()(\w+?://.+?)(?:\))"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        text = node.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(node)
            
        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)
            
            if len(sections[0]) > 0:
                new_nodes.append(
                    TextNode(sections[0], node.text_type)
                )
            
            new_nodes.append(
                TextNode(image[0], TextType.IMAGE, image[1])
            )
            
            text = sections[1]
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        text = node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(node)
            
        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections[0]) > 0:
                new_nodes.append(
                    TextNode(sections[0], node.text_type)
                )
            
            new_nodes.append(
                TextNode(link[0], TextType.LINK, link[1])
            )
            
            text = sections[1]
    
    return new_nodes
