import os, shutil

def copy_files_recursive(source, dest):
    print(f"Copying from {source} to {dest}...")
    
    if not os.path.exists(source) or not os.path.isdir(source):
        raise Exception("source directory doesn't exist")

    if not os.path.exists(dest):
        os.mkdir(dest)        

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(dest, item)
        
        if os.path.isfile(source_path):
            print(f"Copying file {source_path} to {dest_path}...")
            shutil.copy(source_path, dest)
        else:
            print(f"Creating subdirectory {dest_path}...")
            os.mkdir(dest_path)
            copy_files_recursive(source_path, dest_path)

