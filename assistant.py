from ollama import chat, ChatResponse

# Función para consultar el modelo de lenguaje con un contexto de base de conocimiento
def query_model(query: str, knowledge_base: str) -> str:
    # Preparar el prompt con el conocimiento
    prompt = f"Use the following information to answer the question:\n\n{knowledge_base}\n\nQuestion: {query}\nAnswer:"

    # Hacer la consulta al modelo de lenguaje
    response: ChatResponse = chat(model='llama3.2:1b', messages=[{
        'role': 'user',
        'content': prompt
    }])

    # Devolver la respuesta del modelo
    return response.message.content


