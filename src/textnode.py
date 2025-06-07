from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type=TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        if self.text == value.text and self.text_type == value.text_type and self.url == value.url:
            return True
        return False
    
    def __repr__(self):
        if self.url == None:
            return f"TextNode({self.text}, {self.text_type})"
        else:
            return f"TextNode({self.text}, {self.text_type}, {self.url})"