#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Automate
#
# Gwendolyn Dmitruk; 2025
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This program can be saved anywhere; directories should be hard-coded
# This program will trigger s_cat.py to run any time there is a change detected 
# in the number of files held in a directory (like any time new .sbd files are added)
# To start this program, click on its icon, or "python3 automate.py' in wsl ubuntu
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Import libraries

import os
import time
import subprocess


# Directories to monitor

dirs = {
    "/mnt/MetData/Base Camp": {"count": None},
    "/mnt/MetData/Camp 2": {"count": None}
}

# Check interval in seconds (1 minute)
interval = 1 * 60

def count_files(directory):
    """Return the number of files in the directory (not including subdirs)."""
    try:
        return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    except Exception as e:
        print(f"Error reading {directory}: {e}")
        return -1

def run_script(directory):
    """Run s_cat.py in the specified directory."""
    script_path = os.path.join(directory, "s_cat.py")
    try:
        subprocess.run(["python3", script_path], check=True)
        print(f"Ran {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")

def main():
    print("Monitoring started. Press Ctrl+C to stop.")
    while True:
        for dir_path in dirs:
            current_count = count_files(dir_path)
            if current_count != dirs[dir_path]["count"]:
                print(f"Change detected in {dir_path}. File count: {current_count}")
                dirs[dir_path]["count"] = current_count
                run_script(dir_path)
        time.sleep(interval)

if __name__ == "__main__":
    main()

