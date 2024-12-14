from ollama import chat, ChatResponse
from chain_of_thought import chain_of_thought

# Función para consultar el modelo de lenguaje con un contexto de base de conocimiento
def query_model(query: str, knowledge_base: str, model: str) -> str:   
    """
    Consulta el modelo de lenguaje utilizando un contexto de base de conocimiento
    y genera una respuesta con lenguaje natural y razonado.

    Args:
        query (str): La pregunta del usuario que debe ser respondida.
        knowledge_base (str): La base de conocimiento que se debe usar para responder.

    Returns:
        str: La respuesta generada por el modelo de lenguaje.
    """

    # Hacer la consulta al modelo de lenguaje
     # Contexto para generar respuestas interpretativas
    system_context = (
        "You are a thoughtful and knowledgeable assistant. Use the following knowledge base to help the user with their question. "
        "Your responses should not only answer the question but also explain the reasoning behind the answer. "
        "Structure your response to include:"
        "1. A step-by-step explanation of how you arrived at the answer."
        "2. Possible errors or misconceptions and why they are incorrect."
        "3. A clear and concise answer to the user's question at the end."
        "Focus on clarity and simplicity, using short paragraphs and avoiding unnecessary filler. "
        "If the question is unclear or unanswerable, explain why and suggest improvements to the question."
    )

    try:
        # Hacer la consulta al modelo de lenguaje
        response: ChatResponse = chat(
            model=model,
            messages=[
                {'role': 'system', 'content': system_context},
                {'role': 'system', 'content': f"Knowledge Base:\n{knowledge_base}\n"},
                {'role': 'user', 'content': f"User's Question: {query}\n"}
            ]
        )
        # Devolver la respuesta del modelo
        response = response.message.content.strip()
        refined_response = chain_of_thought(response, model)
        return refined_response
    except Exception as e:
        return f"An error occurred while querying the model: {e}"

