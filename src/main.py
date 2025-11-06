import os, shutil

from copystatic import copy_files_recursive
from generatepages import generate_pages_recursive

static_dir_path = "./static"
public_dir_path = "./public"

content_path = "./content/"
template_path = "./template.html"



def main():
    if os.path.exists(public_dir_path):
        shutil.rmtree(public_dir_path)
    copy_files_recursive(static_dir_path, public_dir_path)
    
    generate_pages_recursive(content_path, template_path, public_dir_path)



if __name__ == "__main__":
    main()
