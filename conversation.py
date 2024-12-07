#conversation.py
from ollama import chat, ChatResponse

# Extraer conocimiento relevante de una conversación
def extract_knowledge(user_query: str, assistant_answer: str) -> str:
    """
    Utiliza un modelo de lenguaje para extraer conocimiento útil de una conversación
    combinando la pregunta del usuario y la respuesta del asistente.

    Args:
        user_query (str): La pregunta formulada por el usuario.
        assistant_answer (str): La respuesta proporcionada por el asistente.

    Returns:
        str: Conocimiento relevante extraído de la conversación, en formato de texto.
    """
    # Prompt para extraer conocimiento
    prompt = f"""
    Extract useful, new, or relevant knowledge from the following dialogue:
    - User: {user_query}
    - Assistant: {assistant_answer}
    
    Only include verifiable facts or new information not already known. 
    Provide the output in clear, concise sentences suitable for adding to a knowledge base.
    Avoid including generic statements or repeating existing knowledge.
    """
    
    # Consultar el modelo de lenguaje para extraer el conocimiento
    response: ChatResponse = chat(
        model="llama3.2:1b",
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    # Devolver el conocimiento relevante
    return response.message.content.strip()

# Actualizar la base de conocimiento con información nueva
def update_knowledge_base(knowledge_base: str, new_info: str) -> str:
    """
    Actualiza la base de conocimiento agregando nueva información si no está ya presente.

    Args:
        knowledge_base (str): La base de conocimiento actual.
        new_info (str): La nueva información a agregar.

    Returns:
        str: La base de conocimiento actualizada.
    """
    if new_info and new_info not in knowledge_base:
        return knowledge_base + "\n" + new_info
    return knowledge_base
