import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from common import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestGeneral(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_delimiter(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is a **bold** text node", TextType.TEXT)
        node3 = TextNode("This is an _italic_ text node", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node, node2, node3], "_", TextType.ITALIC), [TextNode("This is a bold text node", TextType.BOLD), TextNode("This is a **bold** text node", TextType.TEXT), TextNode("This is an ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" text node", TextType.TEXT)])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://google.com)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://google.com)")
        self.assertListEqual([("link", "https://google.com")], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://google.com) and [another link](https://boot.dev)")
        self.assertListEqual([("link", "https://google.com"), ("another link", "https://boot.dev")], matches)

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes)

    def test_split_links(self):
        node = TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes)
    
    def test_split_all(self):
        node = TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        node2 = TextNode("This is a second text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and an ![image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
                TextNode("This is a second text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT), 
                TextNode("text", TextType.BOLD), 
                TextNode(" with an ", TextType.TEXT), 
                TextNode("italic", TextType.ITALIC), 
                TextNode(" word and a ", TextType.TEXT), 
                TextNode("code block", TextType.CODE), 
                TextNode(" and an ", TextType.TEXT), 
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
                TextNode(" and a ", TextType.TEXT), 
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes)
    
    def test_more_text_to_textnodes(self):
        text = "This is _more_ **text** with _italic_ words and a `code` **block** and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and ![another image](https://i.imgur.com/3elNhQu.png)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT), 
                TextNode("more", TextType.ITALIC),
                TextNode(" ", TextType.TEXT), 
                TextNode("text", TextType.BOLD), 
                TextNode(" with ", TextType.TEXT), 
                TextNode("italic", TextType.ITALIC), 
                TextNode(" words and a ", TextType.TEXT), 
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT), 
                TextNode("block", TextType.BOLD),  
                TextNode(" and an ", TextType.TEXT), 
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
                TextNode(" and a ", TextType.TEXT), 
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes)
