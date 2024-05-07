from htmlnode import LeafNode
import re


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

    def __repr__(self) -> str:
        text = f'text: "{self.text}"\n'
        text += f'text_type: "{self.text_type}"\n'
        if self.url:
            text += f'url: "{self.url}"\n'
        return text
        
    def __eq__(self, other) -> bool:
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False

def extract_markdown_images(text):
    image_texts = re.findall(r"!\[.*?\]\(.*?\)", text)
    images = []
    for image_text in image_texts:
        images.extend(re.findall(r"\[(.*?)\]\((.*?)\)", image_text))
    return images

def extract_markdown_links(text):
    link_texts = re.findall(r"(?<!!)\[.*?\]\(.*?\)", text)
    links = []
    for link_text in link_texts:
        links.extend(re.findall(r"\[(.*)\]\((.*)\)", link_text)) 
    return links

def split_nodes_delimiter(old_nodes: [TextNode], delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
        elif old_node.text.count(delimiter)%2:
            raise Exception("Invalid Markdown syntax")
        else:
            # print(old_node.text.split(delimiter))
            for i, text in enumerate(old_node.text.split(delimiter)):
                if text == '':
                    continue
                elif not i%2:
                    new_nodes.append(TextNode(text, text_type_text))
                else:
                    new_nodes.append(TextNode(text, text_type))

    return new_nodes

def split_nodes_image(old_nodes: [TextNode]):
    pattern = r"!\[.*?\]\(.*?\)"
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        start_pos = 0
        check_images_exist = re.search(pattern, old_node.text)
        if check_images_exist is None:
            new_nodes.append(old_node)
        else:
            for image in re.finditer(pattern, old_node.text):
                text_node_text = old_node.text[start_pos:image.start()]
                image_node_text = old_node.text[image.start():image.end()]
                start_pos = image.end()
                if text_node_text:
                    new_nodes.append(TextNode(text_node_text, text_type_text))
                image_text, image_link = extract_markdown_images(image_node_text)[0]
                new_nodes.append(TextNode(image_text, text_type_image, image_link))
            text_node_text = old_node.text[start_pos:]
            if text_node_text:
                new_nodes.append(TextNode(text_node_text, text_type_text))

    return new_nodes

def split_nodes_link(old_nodes: [TextNode]):
    pattern = r"(?<!!)\[.*?\]\(.*?\)"
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        start_pos = 0
        check_links_exist = re.search(pattern, old_node.text)
        if check_links_exist is None:
            new_nodes.append(old_node)
        else:
            for link in re.finditer(pattern, old_node.text):
                text_node_text = old_node.text[start_pos:link.start()]
                link_node_text = old_node.text[link.start():link.end()]
                # print(text_node_text, link_node_text)
                start_pos = link.end()
                if text_node_text:
                    new_nodes.append(TextNode(text_node_text, text_type_text))
                link_text, link_link = extract_markdown_links(link_node_text)[0]
                new_nodes.append(TextNode(link_text, text_type_link, link_link))
            text_node_text = old_node.text[start_pos:]
            if text_node_text:
                new_nodes.append(TextNode(text_node_text, text_type_text))
    return new_nodes

def text_to_textnodes(text):
    text_nodes = [TextNode(text, text_type_text)]
    text_nodes = split_nodes_delimiter(text_nodes, '**', text_type_bold)
    text_nodes = split_nodes_delimiter(text_nodes, '*', text_type_italic)
    text_nodes = split_nodes_delimiter(text_nodes, '`', text_type_code)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes
    
def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == text_type_text:
        return LeafNode(None, value=text_node.text)

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


