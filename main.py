import click
import tempfile
from assistant import query_model
from knowledge_base import load_knowledge_base
from rag import rag, rag_query


@click.command()
@click.argument("knowledge_base_file", type=click.Path(exists=True))
@click.option(
    "--model", default="llama3.2:1b", help="Select the language model to use."
)
@click.option("--verbose", is_flag=True, help="Enable detailed output for debugging.")
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

    if verbose:
        click.echo(f"[INFO] Processing data from {knowledge_base_file}...")

    entities = rag(knowledge_base, model)

    # Crear un archivo temporal que se elimina automáticamente al finalizar el programa
    with tempfile.NamedTemporaryFile(
        delete=True, mode="w+", encoding="utf-8", suffix=".txt"
    ) as conversation_file:

        # Bucle de conversación
        while True:
            # Obtener la consulta del usuario
            query = click.prompt("You", type=str)

            # Salir si el usuario escribe 'exit'
            if query.lower() == "exit":
                print("Goodbye! Have a nice day!")
                break

            if verbose:
                click.echo(f"[INFO] Query received: {query}")
                click.echo(f"[INFO] Querying the model {model}...")

            if verbose:
                click.echo(f"[INFO] Processing query...")

            # Leer el archivo temporal y agregar el historial de la conversación
            conversation_context = ""
            try:
                conversation_file.seek(0)  # Volver al inicio del archivo
                conversation_context = (
                    conversation_file.read()
                )  # Leer el contenido del archivo
            except FileNotFoundError:
                # Si el archivo no existe (en el primer ciclo) no pasa nada
                pass

            # Crear un nuevo contexto de conversación con la pregunta del usuario
            conversation_context += f"You: {query}\n"

            relevant_info = rag_query(query, entities, model)

            # Generar la respuesta del asistente utilizando el modelo de lenguaje
            answer = query_model(query, relevant_info, conversation_context, model)

            # Mostrar la respuesta del asistente
            print(f"Assistant: {answer}\n")

            # Guardar la nueva entrada de la conversación en el archivo
            conversation_file.write(f"You: {query}\n")
            conversation_file.write(f"Assistant: {answer}\n")


if __name__ == "__main__":
    main()
