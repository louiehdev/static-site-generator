import re

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocktype import BlockType, markdown_to_blocks, block_to_blocktype, get_header_number

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Not a recoginized text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delimiters = ["**", "_", "`"]
    if not old_nodes:
        raise Exception("No nodes to split")
    if delimiter not in delimiters:
        raise Exception("Not valid markdown syntax")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            for i in range(len(split_text)):
                if i % 2 != 0:
                    new_nodes.append(TextNode(split_text[i], text_type))
                else:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def extract_title(markdown):
    title = re.findall(r"^[^#]*# (.*)", markdown)
    if not title:
        raise Exception("No title found in markdown")
    return title[0].strip("# ")

def split_nodes_image(old_nodes):
    new_nodes = []
    if len(old_nodes) < 1:
        raise Exception("No nodes to split")
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if images: 
            text = node.text
            start_index = 0
            end_index = 1
            for image in images:
                substring = f"![{image[0]}]({image[1]})"
                start_index = text.find(substring)
                end_index = start_index + len(substring)
                new_nodes.append(TextNode(text[:start_index], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                text = text[end_index:]
            if text:
                new_nodes.append(TextNode(text[:end_index], TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    if len(old_nodes) < 1:
        raise Exception("No nodes to split")
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if links: 
            text = node.text
            start_index = 0
            end_index = 1
            for link in links:
                substring = f"[{link[0]}]({link[1]})"
                start_index = text.find(substring)
                end_index = start_index + len(substring)
                new_nodes.append(TextNode(text[:start_index], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                text = text[end_index:]
            if text:
                new_nodes.append(TextNode(text[:end_index], TextType.TEXT))
        else:
            new_nodes.append(node)
               
    return new_nodes

def text_to_textnodes(text):
    return split_nodes_image(split_nodes_link(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    [TextNode(text, TextType.TEXT)], "**", TextType.BOLD), "_", TextType.ITALIC), "`", TextType.CODE)))

def markdown_to_htmlnode(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        match block_to_blocktype(block):
            case BlockType.PARAGRAPH:
                child_nodes.append(ParentNode("p", text_to_children(block, BlockType.PARAGRAPH)))
            case BlockType.HEADING:
                header_number = f"h{get_header_number(block)}"
                child_nodes.append(ParentNode(header_number, text_to_children(block, BlockType.HEADING)))
            case BlockType.CODE:
                joined_string = "".join(block.splitlines(True))
                joined_string = ((joined_string.strip()).strip('```')).lstrip()
                child_nodes.append(ParentNode("pre", [text_node_to_html_node(TextNode(joined_string, TextType.CODE))]))
            case BlockType.QUOTE:
                child_nodes.append(ParentNode("blockquote", text_to_children(block, BlockType.QUOTE)))
            case BlockType.UNORDERED_LIST:
                child_nodes.append(ParentNode("ul", list_to_html(block, BlockType.UNORDERED_LIST)))
            case BlockType.ORDERED_LIST:
                child_nodes.append(ParentNode("ol", list_to_html(block, BlockType.ORDERED_LIST)))
    return ParentNode("div", child_nodes)

def text_to_children(text, blocktype):
    htmlnode_children = []
    formatted_text = ""
    if blocktype is BlockType.PARAGRAPH:
        formatted_text = " ".join(text.splitlines())
    elif blocktype is BlockType.HEADING:
        formatted_text = text.lstrip('# ')
    elif blocktype is BlockType.QUOTE:
        quote_block = text.splitlines()
        quote_list = []
        for quote in quote_block:
            quote_list.append(quote.lstrip('> '))
        formatted_text = " ".join(quote_list)
    elif blocktype is BlockType.UNORDERED_LIST or blocktype is BlockType.ORDERED_LIST:
        formatted_text = text.lstrip('1234567890.- ')

    textnode_children = text_to_textnodes(formatted_text)
    for child in textnode_children:
        htmlnode_children.append(text_node_to_html_node(child))
    return htmlnode_children

def list_to_html(markdown, list_type):
    child_nodes = []
    for split in markdown.splitlines():
        child_nodes.append(ParentNode("li", text_to_children(split, list_type)))
    return child_nodes
