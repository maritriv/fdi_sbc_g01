#rag.py
import click
from ollama import chat, ChatResponse

def rag(knowledge_base: str, model: str): 
    # Divide la base de conocimiento en párrafos
    paragraph = knowledge_base.split("\n\n")
    entities = {}
    for i in range(len(paragraph)):

        # Hacer la consulta al modelo de lenguaje
        try:
            response: ChatResponse = chat(
                model=model,
                messages=[{'role': 'system', 'content': "You are a knowledgeable assistant."
                            "Return me a list with the names of people, places or organizations in this text"
                            f"Knowledge Base:\n{paragraph[i]}\n\n"}]
            )
            # Devolver la respuesta del modelo
            entities_per_paragraph = response.message.content.strip()
        except Exception as e:
            return f"An error occurred while querying the model: {e}"

        
        for e in entities_per_paragraph:
            entities[e] = paragraph[i]

    return entities


def rag_query(query: str, entities, model: str): 
    # Hacer la consulta al modelo de lenguaje
    try:
        response: ChatResponse = chat(
            model=model,
            messages=[{'role': 'system', 'content': "You are a knowledgeable assistant."
                        "Return me a list with the names of people, places or organizations in this text"
                        f"User's Question: {query}\n"}]
        )
        # Devolver la respuesta del modelo
        entities_per_paragraph = response.message.content.strip()
    except Exception as e:
        return f"An error occurred while querying the model: {e}"

    
    answer = ""

    for e in entities_per_paragraph:
        if e in entities:
            answer = answer + entities[e]

    return answer
