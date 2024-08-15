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
                print(f"O Arquivo {remote_file} não existe no repositório remoto. Não será feita a comparação.")
            else:
                with open(local_file, 'r') as lf, open(remote_file, 'r') as rf:
                    local_content = lf.readlines()
                    remote_content = rf.readlines()

                    diff = list(difflib.unified_diff(local_content, remote_content, fromfile=str(local_file), tofile=str(remote_file)))

                    if diff:
                        print(f"Existe diferença entre o conteúdo do arquivo {remote_file} e o arquivo {local_file}. Substituindo pelo Template Remoto")
                        replace_file(local_file, remote_content)
                        print(f"Arquivo {local_file} atualizado com o conteúdo do Template Remoto {remote_file}.")
                        sys.exit(1)
                    else:
                        print(f"{local_file} já está atualizado com o conteúdo do Template Remoto {remote_file}.")

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
