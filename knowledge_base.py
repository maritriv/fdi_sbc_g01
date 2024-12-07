# knowledge_base.py
# Cargar la base de conocimiento desde un archivo
def load_knowledge_base(file_path: str) -> str:
    """
    Carga el contenido de la base de conocimiento desde un archivo de texto.

    Args:
        file_path (str): Ruta del archivo de texto que contiene la base de conocimiento.

    Returns:
        str: El contenido de la base de conocimiento como una cadena de texto.
    """
    with open(file_path, 'r') as file:
        return file.read()

