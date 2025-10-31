import textnode

def main():
    text_node = textnode.TextNode("Lorem Ipsum", textnode.TextType.PLAIN_TEXT, "https://www.boot.dev")
    print(text_node)
    
main()