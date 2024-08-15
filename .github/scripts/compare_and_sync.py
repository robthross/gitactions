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
                        sys.exit(1)
                    else:
                        print(f"{local_file} is already up to date with {remote_file}.")

def sync_files(local_file, local_content, remote_content):
    new_content = []
    remote_lines = {line.strip(): line for line in remote_content}

    for line in local_content:
        stripped_line = line.strip()
        if stripped_line in remote_lines:
            # Substitui a linha local pela linha correspondente do arquivo remoto mantendo a indentação
            indent = len(line) - len(line.lstrip())
            new_content.append(" " * indent + remote_lines[stripped_line])
        else:
            new_content.append(line)

    # Adiciona quaisquer linhas remotas que não estão presentes no arquivo local
    for line in remote_content:
        stripped_line = line.strip()
        if stripped_line not in [l.strip() for l in local_content]:
            new_content.append(line)

    with open(local_file, 'w') as lf:
        lf.writelines(new_content)

def main():
    local_dir = ".github"
    remote_dir = "remote_repo/.github"
    exclude_file = "check-template.yml"
    
    compare_and_sync_file_contents(local_dir, remote_dir, exclude_file)

if __name__ == "__main__":
    main()
