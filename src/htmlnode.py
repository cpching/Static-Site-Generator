class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props={}) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        text = ""

        if self.tag is not None:
            text += f'tag: {self.tag}\n'

        if self.value is not None:
            text += (f'value: {self.value}\n')

        if self.children is not None:
            text += (f'children: \n')
            for child in self.children:
                text += (f'\t{child}\n')

        if bool(self.props):
            text += (f'props\n')
            for attr, val in self.props.items():
                text += (f'{attr}: {val}\n')
        return text

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        attributes = ""

        for attr, val in self.props.items():
            attributes += f' {attr}="{val}"'

        return attributes

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props={}) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        render_text = f'<{self.tag}'
        render_text += self.props_to_html()
        render_text += f'>'

        for child in self.children:
            render_text += child.to_html()

        render_text += f'</{self.tag}>'

        return render_text
        

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props={}) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value

        render_text = f'<{self.tag}'
        render_text += self.props_to_html()
        render_text += f'>{self.value}</{self.tag}>'
        return render_text

        
