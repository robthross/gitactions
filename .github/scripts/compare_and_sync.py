import os
import subprocess
import shutil
from pathlib import Path
import difflib

def compare_directories(local_dir, remote_dir, exclude_file, exclude_file2):
    differences = []
    for root, _, files in os.walk(local_dir):
        for file in files:
            local_file = Path(root) / file
            remote_file = Path(remote_dir) / local_file.relative_to(local_dir)
            
            if local_file.name == exclude_file or exclude_file2:
                continue
            
            if not remote_file.exists():
                differences.append(f"File {remote_file} does not exist in the remote repository.")
            else:
                with open(local_file) as lf, open(remote_file) as rf:
                    local_content = lf.readlines()
                    remote_content = rf.readlines()
                    diff = list(difflib.unified_diff(local_content, remote_content, fromfile=str(local_file), tofile=str(remote_file)))
                    if diff:
                        differences.append(f"Differences found in {local_file}:")
                        differences.extend(diff)
    return differences

def sync_directories(local_dir, remote_dir, exclude_file, exclude_file2):
    for root, _, files in os.walk(remote_dir):
        for file in files:
            if file == exclude_file or exclude_file2:
                continue
            remote_file = Path(root) / file
            local_file = Path(local_dir) / remote_file.relative_to(remote_dir)
            if not local_file.exists() or not filecmp.cmp(local_file, remote_file):
                shutil.copy2(remote_file, local_file)
                print(f"Synced {remote_file} to {local_file}")


def main():
    local_dir = ".github"
    remote_dir = "remote_repo/.github"
    exclude_file = "check-template.yml"
    exclude_file2 = "scripts/compare_and_sync.py"
    
    differences = compare_directories(local_dir, remote_dir, exclude_file, exclude_file2)
    
    if differences:
        print("::error::Differences found between .github directories:")
        for diff in differences:
            print(diff)
        print("::error::Syncing different files from remote repository to local.")
        sync_directories(local_dir, remote_dir, exclude_file, exclude_file2)
        exit(1)
    else:
        print("No differences found between .github directories.")

if __name__ == "__main__":
    main()
