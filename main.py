import click
from assistant import query_model
from knowledge_base import load_knowledge_base
from conversation import extract_knowledge, update_knowledge_base

@click.command()
@click.argument('knowledge_base_file')
def main(knowledge_base_file: str):
    """
    Función principal que maneja la interacción con el usuario y la actualización de la base de conocimiento.
    
    Args:
        knowledge_base_file (str): Ruta del archivo que contiene la base de conocimiento.
    """
    # Cargar la base de conocimiento desde el archivo especificado
    knowledge_base = load_knowledge_base(knowledge_base_file)
    
    print("Hello! I am your virtual assistant. You can ask me anything.")
    print("Type 'exit' to end the conversation.\n")
    
    # Bucle de conversación
    while True:
        # Obtener la consulta del usuario
        query = input("You: ")
        
        # Salir si el usuario escribe 'exit'
        if query.lower() == 'exit':
            print("Goodbye! Have a nice day!")
            break
        
        # Generar la respuesta del asistente utilizando el modelo de lenguaje
        answer = query_model(query, knowledge_base)
        
        # Mostrar la respuesta del asistente
        print(f"Assistant: {answer}\n")
        
        # Extraer nuevo conocimiento de la conversación
        new_knowledge = extract_knowledge(query, answer)
        
        if new_knowledge:
            # Actualizar la base de conocimiento
            knowledge_base = update_knowledge_base(knowledge_base, new_knowledge)
            
            # Guardar la base de conocimiento actualizada sin mostrar mensaje
            with open(knowledge_base_file, 'w') as file:
                file.write(knowledge_base)

if __name__ == "__main__":
    main()
