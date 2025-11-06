import os, shutil
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    if not markdown.startswith("# "):
        raise Exception("markdown does not contain a title")
    
    return markdown[2:].strip()

def generate_page_from_html(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as file:
        markdown = file.read()
    
    with open(template_path) as file:
        template = file.read()
        
    html = markdown_to_html_node(markdown).to_html()
    
    output = template.replace("{{ Title }}", extract_title(markdown)).replace("{{ Content }}", html)
    with open(dest_path, "w") as file:
        file.write(output)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    for item in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
    
    
        if os.path.isfile(content_path):
            print(content_path)
            if content_path.endswith(".md"):
                generate_page_from_html(content_path, template_path, os.path.join(dest_dir_path, item.replace("md", "html")))
            else:
                shutil.copy(content_path, dest_path)  
        else:
            os.mkdir(dest_path)
            generate_pages_recursive(content_path, template_path, dest_path)