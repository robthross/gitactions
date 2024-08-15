import os
from pathlib import Path
import difflib
import sys      

def compare_and_sync_file_contents(local_dir, remote_dir, exclude_file):
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
                        print(f"Differences found in {local_file}. Synchronizing changes...")
                        sync_files(local_file, local_content, remote_content)
                        print(f"Synced {local_file} with {remote_file}.")
                        diferences = True
                    else:
                        print(f"{local_file} is already up to date with {remote_file}.")
    if diferences:
        sys.exit(1)
def sync_files(local_file, local_content, remote_content):
    new_content = []
    diff = list(difflib.ndiff(local_content, remote_content))

    for line in diff:
        if line.startswith("- "):  # Line in local file but not in remote, keep as is.
            new_content.append(line[2:])
        elif line.startswith("+ "):  # Line in remote file but not in local, add it.
            new_content.append(line[2:])
        elif line.startswith("  "):  # Line is the same in both, keep as is.
            new_content.append(line[2:])

    with open(local_file, 'w') as lf:
        lf.writelines(new_content)

def main():
    local_dir = ".github"
    remote_dir = "remote_repo/.github"
    exclude_file = "check-template"
    
    compare_and_sync_file_contents(local_dir, remote_dir, exclude_file)

if __name__ == "__main__":
    main()
