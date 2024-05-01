from htmlnode import LeafNode


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode():
    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True

        else:
            return False

def split_nodes_delimiter(old_nodes: [TextNode], delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
        elif old_node.text.count(delimiter)//2:
            raise Exception("Invalid Markdown syntax")
        else:
            for i, text in enumerate(old_node.split(delimiter)):
                if i//2 and text != '':
                    new_nodes.extend(TextNode(text, text_type_text))
                else:
                    new_nodes.extend(TextNode(text, text_type))


def text_node_to_html_code(text_node: TextNode):
    if text_node.text_type == text_type_text:
        return LeafNode(value=text_node.text)

    elif text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)

    elif text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)

    elif text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)

    elif text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})

    elif text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    else:
        raise Exception(f"Invalid text type: {text_node.text_type}")

