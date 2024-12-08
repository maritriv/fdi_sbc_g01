import click
from assistant import query_model
from knowledge_base import load_knowledge_base

@click.command()
@click.argument('knowledge_base_file', type=click.Path(exists=True))
@click.option('--model', default='llama3.2:1b', help="Select the language model to use.")
@click.option('--verbose', is_flag=True, help="Enable detailed output for debugging.")
def main(knowledge_base_file: str, model: str, verbose: bool):
    """
    Función principal que maneja la interacción con el usuario y la actualización de la base de conocimiento.
    
    Args:
        knowledge_base_file (str): Ruta del archivo que contiene la base de conocimiento.
        model (str): Nombre del modelo de lenguaje a utilizar.
        verbose (bool): indicador para habilitar la salida detallada.
    """

    if verbose:
        click.echo(f"[INFO] Loading knowledge base from {knowledge_base_file}...")

    # Cargar la base de conocimiento desde el archivo especificado
    knowledge_base = load_knowledge_base(knowledge_base_file)

    if verbose:
        click.echo(f"[INFO] Knowledge base loaded. Using model: {model}")
    
    print("Hello! I am your virtual assistant. You can ask me anything.")
    print("Type 'exit' to end the conversation.\n")
    
    # Bucle de conversación
    while True:
        # Obtener la consulta del usuario
        query = click.prompt("You", type=str)
        
        # Salir si el usuario escribe 'exit'
        if query.lower() == 'exit':
            print("Goodbye! Have a nice day!")
            break

        if verbose:
            click.echo(f"[INFO] Query received: {query}")
            click.echo(f"[INFO] Querying the model {model}...")
        
        # Generar la respuesta del asistente utilizando el modelo de lenguaje
        answer = query_model(query, knowledge_base, model)
        
        # Mostrar la respuesta del asistente
        print(f"Assistant: {answer}\n")
        

if __name__ == "__main__":
    main()


