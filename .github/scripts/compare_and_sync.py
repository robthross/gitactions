import os
import filecmp
from pathlib import Path
import difflib

def compare_file_contents(local_dir, remote_dir, exclude_file):
    differences = []
    for root, _, files in os.walk(local_dir):
        for file in files:
            local_file = Path(root) / file
            remote_file = Path(remote_dir) / local_file.relative_to(local_dir)

            if local_file.name == exclude_file:
                continue

            if not remote_file.exists():
                differences.append(f"File {remote_file} does not exist in the remote repository.")
            else:
                with open(local_file, 'r') as lf, open(remote_file, 'r') as rf:
                    local_content = lf.readlines()
                    remote_content = rf.readlines()
                    diff = list(difflib.unified_diff(local_content, remote_content, fromfile=str(local_file), tofile=str(remote_file)))
                    if diff:
                        differences.append(f"Differences found in {local_file}:")
                        differences.extend(diff)
    
    return differences

def main():
    local_dir = ".github"
    remote_dir = "remote_repo/.github"
    exclude_file = "check-template.yml"
    
    differences = compare_file_contents(local_dir, remote_dir, exclude_file)
    
    if differences:
        print("::error::Differences found between .github directories:")
        for diff in differences:
            print(diff)
        exit(1)
    else:
        print("No differences found between .github directories.")

if __name__ == "__main__":
    main()
