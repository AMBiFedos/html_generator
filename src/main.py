from textnode import TextNode, TextType
from htmlnode import LeafNode

def main():
    text_node = TextNode("Lorem Ipsum", TextType.TEXT, "https://www.boot.dev")
    print(text_node)
    



if __name__ == "__main__":
    main()
