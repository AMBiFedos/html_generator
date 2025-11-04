import os, shutil

from copystatic import copy_files_recursive


static_dir_path = "./static"
public_dir_path = "./public"


def main():
    if os.path.exists(public_dir_path):
        shutil.rmtree(public_dir_path)
        
    copy_files_recursive(static_dir_path, public_dir_path)


main()
