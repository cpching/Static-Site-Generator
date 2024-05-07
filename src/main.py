# from textnode import TextNode
from logging import raiseExceptions
from re import template
from block import markdown_to_html_node
import os
import shutil

def copy_dir(src, dst):
    if not os.path.exists(src):
        return 

    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for file in os.listdir(src):
        src_file_path = os.path.join(src, file)
        dst_file_path = os.path.join(dst, file)
        if os.path.isfile(src_file_path):
            shutil.copy(src_file_path, dst_file_path)
        else:
            copy_dir(src_file_path, dst_file_path)
            
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            title = (' '.join(line.split(' ')[1:]))
            return title
    raise Exception("All pages need a single h1 header.")



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = open(from_path).read()
    html = open(template_path).read()
    
    html_title = extract_title(markdown)

    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    html = html.replace("{{ Title }}", html_title)
    html = html.replace("{{ Content }}", html_content)

    print(html)



def main():
    copy_dir('../static', '../public')
    generate_page('../content/index.md', "../template.html", "")

main()

