import click
from assistant import query_model
from knowledge_base import load_knowledge_base



@click.command()
@click.argument('knowledge_base_file')
def main(knowledge_base_file: str):
    # Cargar la base de conocimiento desde el archivo especificado
    knowledge_base = load_knowledge_base(knowledge_base_file)
    
    print("Hello! I am your virtual assistant. You can ask me anything.")
    print("Type 'exit' to end the conversation.\n")
    
    # Bucle para mantener la conversación
    while True:
        # Obtener la consulta del usuario
        query = input("You: ")
        
        # Salir de la conversación si el usuario escribe 'exit'
        if query.lower() == 'exit':
            print("Goodbye! Have a nice day!")
            break
        
        # Realizar la consulta al modelo con la base de conocimiento y la consulta del usuario
        answer = query_model(query, knowledge_base)
        
        # Mostrar la respuesta del modelo
        print(f"Assistant: {answer}\n")

if __name__ == "__main__":
    main()
