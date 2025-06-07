

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode(Tag:{self.tag}, Value:{self.value}, Children:{self.children}, Props:{self.props})"
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        props = self.props.copy()
        prop_list = []
        for prop in props:
            prop_list.append(f" {prop}={props[prop]}")
        return "".join(prop_list)
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError()
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag found")
        if self.children == None:
            raise ValueError("No children found")
        base = ""
        for child in self.children:
            base += child.to_html()
        return f"<{self.tag}>{base}</{self.tag}>"
        