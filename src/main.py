from textnode import TextNode, TextType
from htmlnode import LeafNode

def main():
    text_node = TextNode("Lorem Ipsum", TextType.TEXT, "https://www.boot.dev")
    print(text_node)
    

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("Invalid TextType")

    text = text_node.text
    tag = text_node.text_type.value
    props = None
    if text_node.text_type == TextType.LINK:
        props = {"href": text_node.url}
    if text_node.text_type == TextType.IMAGE:
        props = {"src": text_node.url, "alt": text}
        text = ""
    
    return LeafNode(tag, text, props)

if __name__ == "__main__":
    main()
