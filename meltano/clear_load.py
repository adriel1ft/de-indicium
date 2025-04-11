import os
import shutil

def clear_load_directory(directory_path):
    """
    Remove todos os arquivos e subdiretórios dentro do diretório especificado.
    """
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove arquivos e links simbólicos
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove diretórios e seus conteúdos
            except Exception as e:
                print(f"Erro ao apagar {file_path}: {e}")
        print(f"Diretório '{directory_path}' limpo com sucesso!")
    else:
        print(f"O diretório '{directory_path}' não existe.")

if __name__ == "__main__":
    load_dir = "load/"
    clear_load_directory(load_dir)