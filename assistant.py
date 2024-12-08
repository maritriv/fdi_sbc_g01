from ollama import chat, ChatResponse

# Función para consultar el modelo de lenguaje con un contexto de base de conocimiento
def query_model(query: str, knowledge_base: str) -> str:
    """
    Consulta el modelo de lenguaje utilizando un contexto de base de conocimiento
    y genera una respuesta con lenguaje natural y razonado.

    Args:
        query (str): La pregunta del usuario que debe ser respondida.
        knowledge_base (str): La base de conocimiento que se debe usar para responder.

    Returns:
        str: La respuesta generada por el modelo de lenguaje.
    """
    # Construir un prompt enfocado en respuestas naturales pero precisas
    prompt = (
        "You are a knowledgeable assistant. Use the following knowledge base to answer the user's question. "
        "Respond clearly and directly, but in a conversational tone. Avoid bullet points or numbered lists unless necessary. "
        "Focus on delivering a helpful and accurate answer in fluent English, while maintaining a natural flow.\n\n"
        f"Knowledge Base:\n{knowledge_base}\n\n"
        f"User's Question: {query}\n"
        "Answer (in natural, conversational style):"
    )

    # Hacer la consulta al modelo de lenguaje
    response: ChatResponse = chat(model='llama3.2:1b', messages=[{
        'role': 'user',
        'content': prompt
    }])

    # Devolver la respuesta del modelo
    return response.message.content.strip()

