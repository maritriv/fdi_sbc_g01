# main.py

import click
from base_conocimiento import cargar_base_conocimiento
from consulta import leer_consulta, ejecutar_consulta
from utils import imprimir_tabla

@click.command()
@click.argument('archivo_base_conocimiento')
def main(archivo_base_conocimiento):
    # Cargar la base de conocimiento desde el archivo especificado
    base_conocimiento = cargar_base_conocimiento(archivo_base_conocimiento)

    while True:
        # Leer el comando de entrada del usuario
        comando = input("SBC_P3> ").strip()
        
        if comando.startswith("select") or comando.startswith("SELECT"):
            try:
                # Procesar la consulta con leer_consulta para obtener su estructura
                consulta_parsed = leer_consulta(comando)

                # Ejecutar la consulta en la base de conocimiento usando la estructura obtenida
                resultados = ejecutar_consulta(base_conocimiento, consulta_parsed)

                # Imprimir los resultados en formato tabla
                imprimir_tabla(resultados, consulta_parsed['variables'])

            except ValueError as e:
                click.echo(f"Error en la consulta: {e}")

        elif comando.startswith("exit"):
            break

        else:
            click.echo("Comando no reconocido")

if __name__ == '__main__':
    main()

