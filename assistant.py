#assistant.py
from ollama import chat, ChatResponse

# Función para consultar el modelo de lenguaje con un contexto de base de conocimiento
def query_model(query: str, knowledge_base: str) -> str:
    """
    Consulta el modelo de lenguaje utilizando un contexto de base de conocimiento.

    Args:
        query (str): La pregunta del usuario que debe ser respondida.
        knowledge_base (str): La base de conocimiento que se debe usar para responder.

    Returns:
        str: La respuesta generada por el modelo de lenguaje.
    """
    # Preparar el prompt con el conocimiento
    prompt = f"Use the following information to answer the question:\n\n{knowledge_base}\n\nQuestion: {query}\nAnswer:"

    # Hacer la consulta al modelo de lenguaje
    response: ChatResponse = chat(model='llama3.2:1b', messages=[{
        'role': 'user',
        'content': prompt
    }])

    # Devolver la respuesta del modelo
    return response.message.content
