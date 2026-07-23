#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Upload to Github
#
# Gwendolyn Dmitruk; 2025
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This program pushes products to github
# Triggered by s_cat.py after t_rh_10.py
# A copy should be in every folder
# where iridium data is processed



# Import libraries

import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from itertools import chain


# Define paths

source_dir = Path("/mnt/MetData/Base Camp")
dest_dir = Path.home() / "MetData_"  # GitHub repo path in WSL home


# Ensure paths exist

if not source_dir.exists():
    raise FileNotFoundError("Source directory does not exist.")
if not dest_dir.exists():
    raise FileNotFoundError("GitHub repo directory does not exist.")


# Copy all .csv files

print("Copying .csv files...")
for pattern in ("*.csv", "*.png"):
    for file in source_dir.glob(pattern):
        shutil.copyfile(file, dest_dir / file.name)


# Run git commands

def run_git_command(command, cwd):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {' '.join(command)}:\n{result.stderr}")
    else:
        print(f"Ran: {' '.join(command)}")


# Git operations

print("Running Git operations...")
run_git_command(["git", "add", "."], cwd=dest_dir)
commit_message = f"Auto-upload: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
print("Running Git operations...")
run_git_command(["git", "add", "."], cwd=dest_dir)
commit_message = f"Auto-upload: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
run_git_command(["git", "commit", "-m", commit_message], cwd=dest_dir)
run_git_command(["git", "pull", "--rebase"], cwd=dest_dir)
run_git_command(["git", "push", "origin", "main"], cwd=dest_dir)