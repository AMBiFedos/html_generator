from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    IMAGE_TEXT = "image"

class TextNode():
    
    def __init__(self, text: str, text_type: TextType, url: str):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, value):
        if self.text == value.text and self.text_type == value.text_type and self.url == value.url:
            return True

        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    