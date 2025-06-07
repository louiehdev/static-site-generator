import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode(None, None, None, {"href": "https://www.boot.dev", "target": "_blank",})
        print(node)
        print(node2.props_to_html())
        self.assertEqual(node.props_to_html()[:1], " ")
    
    def test_leaf_to_html(self):
        node = LeafNode("p", "Yeehaw")
        node2 = LeafNode("a", "Click this link", {"href": "https://www.boot.dev"})
        print(node2.to_html())
        self.assertEqual(node.to_html(), "<p>Yeehaw</p>")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_many_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("b", "child2")
        child_node3 = LeafNode("p", "child3")
        parent_node = ParentNode("div", [child_node, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b>child2</b><p>child3</p></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>",)

if __name__ == "__main__":
    unittest.main()