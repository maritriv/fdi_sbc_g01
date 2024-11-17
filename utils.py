# utils.py

import click
from comandos import load, add, delete, save, help, draw
from consulta import leer_consulta, ejecutar_consulta

# Funciones de salida de datos:


def imprimir_tabla(resultados, variables):
    """
    Imprime los resultados en formato de tabla alineada.
    """
    if resultados:
        column_widths = {var: max(len(var), 14) for var in variables}

        encabezado = " | ".join(f"?{var:{column_widths[var]}}" for var in variables)
        separador = "-+-".join("-" * column_widths[var] for var in variables)

        click.echo(encabezado)
        click.echo(separador)

        for resultado in resultados:
            fila = " | ".join(
                f"{resultado.get(var, ''):{column_widths[var]}}" for var in variables
            )
            click.echo(fila)
    else:
        click.echo("No se encontraron resultados para la consulta.")


def imprimir_conocimiento(base_conocimiento):
    """
    Imprime toda la base de conocimiento.

    :param base_conocimiento: La base de conocimiento actual.
    """
    imprimir_base_conocimiento(base_conocimiento)


def imprimir_base_conocimiento(base_conocimiento):
    """
    Imprime todas las tripletas de la base de conocimiento con un formato alineado.
    """
    if not base_conocimiento:
        print("La base de conocimiento está vacía.")
        return

    # Imprimir encabezado
    print(f"{'Sujeto':<20} {'Verbo':<20} {'Objeto'}")
    print("=" * 60)

    # Imprimir cada tripleta
    for tripleta in base_conocimiento:
        if len(tripleta) == 3:
            sujeto, verbo, objeto = tripleta
            # Imprimir las tripletas con espacio alineado
            print(f"{sujeto:<20} {verbo:<20} {objeto}")


# Función para procesar una consulta
def procesar_consulta(base_conocimiento, comando):
    """
    Procesa y ejecuta una consulta SPARQL.

    :param base_conocimiento: La base de conocimiento cargada.
    :param comando: La consulta SPARQL.
    """
    try:
        consulta_parsed = leer_consulta(comando)
        resultados = ejecutar_consulta(base_conocimiento, consulta_parsed)
        imprimir_tabla(resultados, consulta_parsed["variables"])
    except ValueError as e:
        click.echo(f"Error en la consulta: {e}")
    return resultados


# Función de control de comandos:
def iniciar_bucle_interactivo(base_conocimiento):
    """
    Inicia el bucle interactivo para recibir comandos del usuario.
    Permite consultas multilínea y guardar la última consulta para dibujar un grafo
    """
    ultima_consulta_resultados = None  # Variable para almacenar los resultados de la última consulta

    while True:
        consulta_completa = "" # Variable para almacenar las consultas multilíneas
        
        while True:
            comando = input("SBC_P3> ").strip()

            # Si el comando es una consulta, verificamos si es multilínea
            if comando.lower().startswith("select") or comando.lower().startswith(
                "construct"
            ):
                # Comenzamos a acumular la consulta
                consulta_completa += comando + "\n"
                # Esperamos más líneas hasta que el usuario termine la consulta
                while not comando.endswith("}"):
                    comando = input("Continúa tu consulta: ").strip()
                    consulta_completa += comando + "\n"

                # Aquí tenemos la consulta completa
                print("Consulta completa recibida:")
                print(consulta_completa)
                # Procesamos la consulta completa
                ultima_consulta_resultados = procesar_consulta(base_conocimiento, consulta_completa)
                break  # Salir del bucle de consultas

            # Comando 'help'
            if comando.lower() == "help":
                help()

            # Procesar comando 'select'
            if comando.lower().startswith("select"):
                procesar_consulta(base_conocimiento, comando)

            # Procesar comando 'load'
            elif comando.lower().startswith("load"):
                base_conocimiento = load(base_conocimiento, comando)

            # Imprimir toda la base de conocimiento
            elif comando.lower() == "print_all" or comando.lower() == "imprimir_todo":
                imprimir_conocimiento(base_conocimiento)

            # Comando de salida
            elif comando.lower() == "exit":
                click.echo("Saliendo del programa...")
                break

            # Procesar comando 'add'
            elif comando.lower().startswith("add"):
                # Llamar a la función add y pasar el comando para su procesamiento
                add(base_conocimiento, comando)

            # Procesar comando 'delete'
            elif comando.lower().startswith("delete"):
                base_conocimiento = delete(base_conocimiento, comando)

            # Procesar comando 'save'
            elif comando.lower().startswith("save"):
                base_conocimiento = save(base_conocimiento, comando)

            # Comando 'draw' para graficar la última consulta
            elif comando.lower() == "draw":
                if ultima_consulta_resultados:
                    draw(ultima_consulta_resultados)
                else:
                    click.echo("No se ha realizado ninguna consulta aún o la consulta no ha producido resultados.")

            # Comando no reconocido
            else:
                click.echo(
                    "Comando no reconocido. Usa una consulta SPARQL válida o 'exit' para salir."
                )
