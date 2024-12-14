# chain_of_thought.py

from ollama import chat, ChatResponse


# Función para consultar el modelo de lenguaje con un contexto de base de conocimiento
def chain_of_thought(response: str, model: str) -> str:
    """
    Consulta el modelo de lenguaje utilizando un contexto de base de conocimiento
    y genera una respuesta con lenguaje natural y razonado.

    Args:
        response (str): La respuesta que se dió al pensar por primera vez

    Returns:
        str: La respuesta generada por el modelo de lenguaje.
    """

    # Hacer la consulta al modelo de lenguaje
    system_context = (
        "You are a knowledgeable assistant. Your task is to refine the following response, which may be hesitant or incomplete, "
        "to make it precise, confident, and clear. Focus on resolving any doubts present in the original response and provide a "
        "concise and definitive answer. Avoid repeating unnecessary details or including filler content."
    )

    try:
        # Hacer la consulta al modelo de lenguaje
        refined_response: ChatResponse = chat(
            model=model,
            messages=[
                {"role": "system", "content": system_context},
                {"role": "user", "content": f"Previous Response: {response}\n"},
            ],
        )

        # Devolver la respuesta refinada
        return refined_response.message.content.strip()
    except Exception as e:
        return f"An error occurred while querying the model: {e}"
