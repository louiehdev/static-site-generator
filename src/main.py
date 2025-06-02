from textnode import TextNode, TextType

def main():
    testnode = TextNode("This is text", TextType.LINK, "https://www.boot.dev")
    print(testnode)

main()