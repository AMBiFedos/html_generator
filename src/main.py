import os, shutil, sys

from copystatic import copy_files_recursive
from generatepages import generate_pages_recursive

static_dir_path = "./static"
public_dir_path = "./docs"

content_path = "./content/"
template_path = "./template.html"



def main():
    basepath = sys.argv[1]
    
    if os.path.exists(public_dir_path):
        shutil.rmtree(public_dir_path)
    copy_files_recursive(static_dir_path, public_dir_path)
    
    generate_pages_recursive(content_path, template_path, public_dir_path, basepath)



if __name__ == "__main__":
    main()
