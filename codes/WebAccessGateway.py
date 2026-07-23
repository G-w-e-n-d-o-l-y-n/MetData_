#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Web Access Gateway
#
# Gwendolyn Dmitruk; 2025
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This program will be triggered by s_cat.py after upload.py
# Copies the contents of the directory
# into a diffrernt (in this case, web-accessible) directory
# a copy of this program should be in every folder
# where iridium data is processed
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Import libraries

#!/usr/bin/env python3
import os
import time
import shutil
from datetime import datetime


# Folder Configuration

DEST_DIR = "/mnt/root/MET/Everest/BaseCamp"  
INTERVAL_MINUTES = 5               # Time between copying

def copy_directory(src, dst):
    """Copy contents of src directory into dst directory."""
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)
        if os.path.isdir(src_item):
            shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
        else:
            shutil.copy2(src_item, dst_item)

def main():
    src = os.getcwd()
    print(f"Starting auto-copy service.")
    print(f"Source: {src}")
    print(f"Destination: {DEST_DIR}")
    print(f"Interval: {INTERVAL_MINUTES} minutes")

    while True:
        try:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Copying files...")
            copy_directory(src, DEST_DIR)
            print("Copy complete.")
        except Exception as e:
            print(f"Error during copy: {e}")
        
        time.sleep(INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()
