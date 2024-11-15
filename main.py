import click
from base_conocimiento import cargar_multiples_bases_conocimiento
from consulta import leer_consulta, ejecutar_consulta
from utils import imprimir_tabla

@click.command()
@click.argument('archivos_base_conocimiento', nargs=-1)  # Acepta uno o más archivos
def main(archivos_base_conocimiento):
    """
    Programa principal para cargar bases de conocimiento y ejecutar consultas.
    
    ARCHIVOS_BASE_CONOCIMIENTO: Uno o más archivos de base de conocimiento.
    """
    if not archivos_base_conocimiento:
        click.echo("Debes especificar al menos un archivo de base de conocimiento.")
        return

    try:
        # Cargar y combinar las bases de conocimiento
        base_conocimiento = cargar_multiples_bases_conocimiento(archivos_base_conocimiento)
    except FileNotFoundError as e:
        click.echo(f"Error al cargar los archivos: {e}")
        return

    # Iniciar el bucle interactivo de consultas
    while True:
        comando = input("SBC_P3> ").strip()
        
        if comando.startswith("select") or comando.startswith("SELECT"):
            try:
                # Procesar la consulta
                consulta_parsed = leer_consulta(comando)
                resultados = ejecutar_consulta(base_conocimiento, consulta_parsed)
                imprimir_tabla(resultados, consulta_parsed['variables'])
            except ValueError as e:
                click.echo(f"Error en la consulta: {e}")
        elif comando.lower() == "exit":
            click.echo("Saliendo del programa...")
            break
        else:
            click.echo("Comando no reconocido. Usa una consulta SPARQL válida o 'exit' para salir.")

if __name__ == '__main__':
    main()
