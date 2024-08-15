import os
from pathlib import Path
import sys
import difflib

def compare_and_replace_file_contents(local_dir, remote_dir, exclude_file):
    for root, _, files in os.walk(local_dir):
        for file in files:
            local_file = Path(root) / file
            remote_file = Path(remote_dir) / local_file.relative_to(local_dir)

            if local_file.name == exclude_file:
                continue

            if not remote_file.exists():
                print(f"File {remote_file} does not exist in the remote repository.")
            else:
                with open(local_file, 'r') as lf, open(remote_file, 'r') as rf:
                    local_content = lf.readlines()
                    remote_content = rf.readlines()

                    diff = list(difflib.unified_diff(local_content, remote_content, fromfile=str(local_file), tofile=str(remote_file)))

                    if diff:
                        print(f"Differences found in {local_file}. Replacing with remote content...")
                        replace_file(local_file, remote_content)
                        print(f"Replaced {local_file} with content from {remote_file}.")
                        sys.exit(1)
                    else:
                        print(f"{local_file} is already up to date with {remote_file}.")

def replace_file(local_file, remote_content):
    with open(local_file, 'w') as lf:
        lf.writelines(remote_content)

def main():
    local_dir = ".github"
    remote_dir = "remote_repo/.github"
    exclude_file = "check-template.yml"
    
    compare_and_replace_file_contents(local_dir, remote_dir, exclude_file)

if __name__ == "__main__":
    main()
