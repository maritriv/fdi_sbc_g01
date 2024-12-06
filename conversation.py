#conversation.py
from ollama import chat, ChatResponse

# Extraer conocimiento relevante de una conversación
def extract_knowledge(user_query: str, assistant_answer: str) -> str:
    """
    Use a language model to extract useful knowledge from the conversation.
    Combine the user's question and the assistant's answer to identify relevant facts.
    """
    # Prompt to extract knowledge
    prompt = f"""
    Extract useful, new, or relevant knowledge from the following dialogue:
    - User: {user_query}
    - Assistant: {assistant_answer}
    
    Only include verifiable facts or new information not already known. 
    Provide the output in clear, concise sentences suitable for adding to a knowledge base.
    Avoid including generic statements or repeating existing knowledge.
    """
    
    # Query the language model to extract knowledge
    response: ChatResponse = chat(
        model="llama3.2:1b",
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    # Return the relevant knowledge
    return response.message.content.strip()

# Actualizar la base de conocimiento con información nueva
def update_knowledge_base(knowledge_base: str, new_info: str) -> str:
    if new_info and new_info not in knowledge_base:
        return knowledge_base + "\n" + new_info
    return knowledge_base

