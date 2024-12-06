# knowledge_base.py

# Cargar la base de conocimiento desde un archivo
def load_knowledge_base(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()